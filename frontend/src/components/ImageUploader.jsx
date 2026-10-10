import { useRef } from 'react'
import { validateFile } from '../utils/imageUtils'
export default function ImageUploader({ onSelect, onInvalid }) {
  const ref = useRef(null)
  const change = (e) => {
    const file = e.target.files?.[0]
    e.target.value = ''
    const problem = validateFile(file)
    if (problem) return onInvalid(problem)
    onSelect(file)
  }
  return (
    <div className="dropzone">
      <label htmlFor="photo">Choose a photo (JPG or PNG, up to 8 MB)</label>
      <input id="photo" ref={ref} type="file" accept="image/jpeg,image/png" onChange={change} className="sr" />
      <button className="btn" onClick={() => ref.current.click()}>Upload photo</button>
    </div>
  )
}
