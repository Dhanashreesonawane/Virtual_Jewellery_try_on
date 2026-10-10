import useCamera from '../hooks/useCamera'
import useLiveTryOn from '../hooks/useLiveTryOn'
import ErrorMessage, { friendly } from './ErrorMessage'

export default function LiveView({ jewelryId, category }) {
  const { videoRef, active, error, start, stop } = useCamera()
  const { frameUrl, meta, state } = useLiveTryOn({ videoRef, enabled: active, jewelryId, category })
  return (
    <div className="camera live">
      {!active && <p className="muted">{error ? friendly(error === 'denied' ? 'CAMERA_DENIED' : 'CAMERA_UNAVAILABLE') : 'Start your camera, then pick a piece. It follows you as you move.'}</p>}
      {active && (
        <div className="stage">
          <video ref={videoRef} autoPlay playsInline muted aria-label="Camera preview" className={frameUrl ? 'hidden-video' : ''} />
          {frameUrl && <img src={frameUrl} alt="Live view with jewellery applied" className="mirror" />}
        </div>
      )}
      <div className="row">
        {!active ? <button className="btn" onClick={start}>Start camera</button>
          : <button className="btn ghost" onClick={stop}>Stop camera</button>}
      </div>
      {active && state === 'closed' && <ErrorMessage code="BACKEND_UNAVAILABLE" />}
      {active && state === 'live' && (
        <dl className="meta" aria-live="polite">
          <div><dt>Tracking</dt><dd>{meta ? (meta.tracking ? 'Locked on' : 'Searching…') : '—'}</dd></div>
          <div><dt>Processing</dt><dd>{meta?.processing_time_ms != null ? `${meta.processing_time_ms} ms` : '—'}</dd></div>
          <div><dt>Processing FPS</dt><dd>{meta?.fps_estimate ?? '—'}</dd></div>
          <div><dt>Stream FPS</dt><dd>{meta?.stream_fps ?? '—'}</dd></div>
        </dl>
      )}
      {meta?.error && <ErrorMessage code={meta.error.code} message={meta.error.message} />}
    </div>
  )
}
