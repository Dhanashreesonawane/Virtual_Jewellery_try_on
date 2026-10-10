import useCamera from '../hooks/useCamera'
import { friendly } from './ErrorMessage'
export default function CameraView({ onCapture }) {
  const { videoRef, active, error, start, stop, capture } = useCamera()
  const take = () => { const f = capture(); if (f) onCapture(f) }
  return (
    <div className="camera">
      {active
        ? <video ref={videoRef} autoPlay playsInline muted aria-label="Live camera preview" />
        : <p className="muted">{error ? friendly(error === 'denied' ? 'CAMERA_DENIED' : 'CAMERA_UNAVAILABLE') : 'Start your camera to capture a frame.'}</p>}
      <div className="row">
        {!active ? <button className="btn" onClick={start}>Start camera</button>
          : <><button className="btn" onClick={take}>Capture frame</button>
              <button className="btn ghost" onClick={stop}>Stop camera</button></>}
      </div>
    </div>
  )
}
