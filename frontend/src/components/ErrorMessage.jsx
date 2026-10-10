const MESSAGES = {
  NO_HAND_DETECTED: 'No suitable hand was detected. Please use an image where your hand is clearly visible.',
  NO_FACE_DETECTED: 'No face was detected. Face the camera with your ears uncovered and try again.',
  NO_POSE_DETECTED: 'We could not see your shoulders. Include your face and shoulders in the frame.',
  NO_EAR_LANDMARKS: 'Your ears could not be located. Try a photo that shows your face straight on.',
  JEWELRY_NOT_FOUND: 'That piece is no longer available. Please choose another.',
  INVALID_IMAGE: 'This image could not be read. Try a different JPG or PNG.',
  UNSUPPORTED_FORMAT: 'Only JPG and PNG images are supported.',
  IMAGE_TOO_LARGE: 'This image is too large. Choose one under 8 MB.',
  EMPTY_UPLOAD: 'The file was empty. Choose another image.',
  BACKEND_UNAVAILABLE: 'The try-on server is not reachable. Check that the backend is running.',
  CAMERA_DENIED: 'Camera access was blocked. Allow it in your browser settings, or upload a photo instead.',
  CAMERA_UNAVAILABLE: 'No camera was found on this device. Upload a photo instead.',
  PROCESSING_FAILED: 'Something went wrong while applying the jewellery. Please try again.',
}
export const friendly = (code, fallback) => MESSAGES[code] || fallback || MESSAGES.PROCESSING_FAILED
export default function ErrorMessage({ code, message, onDismiss }) {
  if (!code && !message) return null
  return (
    <div className="error" role="alert">
      <p>{friendly(code, message)}</p>
      {onDismiss && <button className="link" onClick={onDismiss}>Dismiss</button>}
    </div>
  )
}
