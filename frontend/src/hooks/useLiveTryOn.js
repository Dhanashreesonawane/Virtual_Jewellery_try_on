import { useEffect, useRef, useState } from 'react'
import { wsUrl } from '../services/api'

// Stop-and-wait loop: send a frame, wait for the processed frame, send the next.
// The rate adapts to what the server can actually deliver (no fixed fake FPS).
export default function useLiveTryOn({ videoRef, enabled, jewelryId, category }) {
  const [frameUrl, setFrameUrl] = useState(null)
  const [meta, setMeta] = useState(null)
  const [state, setState] = useState('idle') // idle | connecting | live | closed
  const cfg = useRef({ jewelryId, category })
  const wsRef = useRef(null)

  useEffect(() => {
    cfg.current = { jewelryId, category }
    const ws = wsRef.current
    if (ws?.readyState === 1 && jewelryId) ws.send(JSON.stringify({ jewelry_id: jewelryId, category }))
  }, [jewelryId, category])

  useEffect(() => {
    if (!enabled) { setFrameUrl(null); setMeta(null); setState('idle'); return }
    setState('connecting')
    const ws = new WebSocket(wsUrl())
    wsRef.current = ws
    const canvas = document.createElement('canvas')
    let stopped = false, pendingMeta = null, lastUrl = null, sentCfg = null

    const send = () => {
      if (stopped || ws.readyState !== 1) return
      const v = videoRef.current, c = cfg.current
      if (!v || !v.videoWidth || !c.jewelryId) return void setTimeout(send, 150)
      const key = `${c.jewelryId}|${c.category}`
      if (sentCfg !== key) { ws.send(JSON.stringify({ jewelry_id: c.jewelryId, category: c.category })); sentCfg = key }
      const w = Math.min(640, v.videoWidth)
      canvas.width = w; canvas.height = Math.round((w * v.videoHeight) / v.videoWidth)
      canvas.getContext('2d').drawImage(v, 0, 0, canvas.width, canvas.height)
      canvas.toBlob((b) => b && ws.readyState === 1 && ws.send(b), 'image/jpeg', 0.7)
    }
    ws.onopen = () => { setState('live'); send() }
    ws.onmessage = (e) => {
      if (typeof e.data === 'string') {
        const m = JSON.parse(e.data)
        if (m.type === 'error') { setMeta({ tracking: false, error: m.error }); setTimeout(send, 300) }
        else pendingMeta = m
        return
      }
      setMeta(pendingMeta)
      if (lastUrl) URL.revokeObjectURL(lastUrl)
      lastUrl = URL.createObjectURL(e.data)
      setFrameUrl(lastUrl)
      send()
    }
    ws.onclose = () => { if (!stopped) setState('closed') }
    ws.onerror = () => setState('closed')
    return () => { stopped = true; ws.close(); if (lastUrl) URL.revokeObjectURL(lastUrl) }
  }, [enabled, videoRef])

  return { frameUrl, meta, state }
}
