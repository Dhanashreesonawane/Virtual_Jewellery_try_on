import { useState } from 'react'
import LoadingIndicator from './LoadingIndicator'
export default function TryOnViewer({ before, result, busy, onReset, onSave, onDownload, onShare, note }) {
  const [showBefore, setShowBefore] = useState(false)
  if (!before) return <div className="viewer empty"><p className="muted">Upload a photo or capture a frame to begin.</p></div>
  const shown = result && !showBefore ? result.image_url : before
  return (
    <div className="viewer">
      <div className="stage">
        <img src={shown} alt={result && !showBefore ? 'Your photo with jewellery applied' : 'Your original photo'} />
        {busy && <div className="veil"><LoadingIndicator text="Applying jewellery…" /></div>}
      </div>
      {result && (
        <div className="row" role="group" aria-label="Compare">
          <button className={showBefore ? 'tab' : 'tab on'} onClick={() => setShowBefore(false)}>After</button>
          <button className={showBefore ? 'tab on' : 'tab'} onClick={() => setShowBefore(true)}>Before</button>
        </div>
      )}
      {result && (
        <dl className="meta">
          <div><dt>Jewellery</dt><dd>{result.jewelry_id}</dd></div>
          <div><dt>Category</dt><dd>{result.category}</dd></div>
          <div><dt>Processing time</dt><dd>{result.processing_time_ms} ms</dd></div>
          <div><dt>Estimated FPS</dt><dd>{result.fps_estimate}</dd></div>
          <div><dt>Confidence</dt><dd>{result.confidence}</dd></div>
        </dl>
      )}
      <div className="row">
        <button className="btn ghost" onClick={onReset}>Reset</button>
        {result && <><button className="btn" onClick={onSave}>Save</button>
          <button className="btn" onClick={onDownload}>Download</button>
          <button className="btn" onClick={onShare}>Share</button></>}
      </div>
      {note && <p className="muted" role="status">{note}</p>}
    </div>
  )
}
