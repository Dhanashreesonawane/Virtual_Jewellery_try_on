import { useCallback, useEffect, useState } from 'react'
import LiveView from '../components/LiveView'
import ErrorMessage from '../components/ErrorMessage'
import ImageUploader from '../components/ImageUploader'
import JewelryCategory from '../components/JewelryCategory'
import JewelryGrid from '../components/JewelryGrid'
import LoadingIndicator from '../components/LoadingIndicator'
import TryOnViewer from '../components/TryOnViewer'
import { compressImage, downloadImage, shareImage } from '../utils/imageUtils'
import * as api from '../services/api'

export default function TryOn() {
  const [mode, setMode] = useState(location.hash.includes('mode=upload') ? 'upload' : 'camera')
  const [source, setSource] = useState(null) // {url, file?, dataUrl?}
  const [category, setCategory] = useState('ring')
  const [items, setItems] = useState([])
  const [loadingItems, setLoadingItems] = useState(true)
  const [selected, setSelected] = useState(null)
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)
  const [note, setNote] = useState('')

  useEffect(() => {
    let live = true
    setLoadingItems(true); setSelected(null)
    api.getJewelry(category).then((d) => live && setItems(d))
      .catch((e) => live && setError({ code: e.code, message: e.message }))
      .finally(() => live && setLoadingItems(false))
    return () => { live = false }
  }, [category])

  const setInput = (s) => { setSource(s); setResult(null); setError(null); setNote('') }

  const tryOn = useCallback(async () => {
    if (busy || !source || !selected) return
    setBusy(true); setError(null); setNote('')
    try {
      const data = source.file
        ? await api.tryOnImage(await compressImage(source.file), selected, category)
        : await api.tryOnFrame(source.dataUrl, selected, category)
      setResult(data)
    } catch (e) { setError({ code: e.code, message: e.message }) }
    finally { setBusy(false) }
  }, [busy, source, selected, category])

  const act = (fn, ok) => async () => {
    try { setNote((await fn()) || ok) } catch (e) { setNote(e.message || 'That did not work.') }
  }
  const save = act(async () => { await api.saveResult(result) }, 'Saved to your looks.')
  const download = act(() => downloadImage(result.image_url), 'Download started.')
  const share = act(async () => (await shareImage(result.image_url)) === 'unsupported'
    ? 'Sharing is not supported in this browser. Use Download instead.' : 'Shared.')

  const hint = !source ? 'Add a photo first.' : !selected ? 'Choose a piece.' : ''
  return (
    <main className="tryon">
      <section aria-label="Your photo">
        <div className="tabs" role="tablist" aria-label="Input mode">
          {[['camera', 'Live camera'], ['upload', 'Upload image']].map(([m, l]) => (
            <button key={m} role="tab" aria-selected={mode === m} className={mode === m ? 'tab on' : 'tab'} onClick={() => setMode(m)}>{l}</button>
          ))}
        </div>
        {mode === 'camera'
          ? <LiveView jewelryId={selected} category={category} />
          : <>
              <ImageUploader onInvalid={(m) => setError({ message: m })} onSelect={(file) => setInput({ file, url: URL.createObjectURL(file) })} />
              <TryOnViewer before={source?.url} result={result} busy={busy} note={note}
                onReset={() => setInput(null)} onSave={save} onDownload={download} onShare={share} />
            </>}
      </section>
      <aside aria-label="Choose jewellery">
        <JewelryCategory value={category} onChange={setCategory} />
        {loadingItems ? <LoadingIndicator text="Loading collection…" /> : <JewelryGrid items={items} selectedId={selected} onSelect={setSelected} />}
        {mode === 'upload' ? (<>
          <button className="btn wide" disabled={busy || !source || !selected} onClick={tryOn}>{busy ? 'Applying jewellery…' : 'Try on'}</button>
          {hint && <p className="muted">{hint}</p>}
        </>) : !selected && <p className="muted">Choose a piece to see it follow you live.</p>}
        <ErrorMessage code={error?.code} message={error?.message} onDismiss={() => setError(null)} />
      </aside>
    </main>
  )
}
