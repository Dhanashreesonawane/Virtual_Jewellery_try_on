export default function LoadingIndicator({ text = 'Analyzing your image…' }) {
  return <div className="loading" role="status" aria-live="polite"><span className="ring-spin" aria-hidden="true" />{text}</div>
}
