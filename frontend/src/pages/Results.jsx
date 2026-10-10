import { useEffect, useState } from 'react'
import ErrorMessage from '../components/ErrorMessage'
import LoadingIndicator from '../components/LoadingIndicator'
import { getResults } from '../services/api'
export default function Results() {
  const [rows, setRows] = useState(null)
  const [error, setError] = useState(null)
  useEffect(() => { getResults().then(setRows).catch((e) => setError({ code: e.code, message: e.message })) }, [])
  return (
    <main className="results">
      <h1>Saved looks</h1>
      <ErrorMessage code={error?.code} message={error?.message} />
      {!rows && !error && <LoadingIndicator text="Loading…" />}
      {rows?.length === 0 && <p className="muted">Nothing saved yet. <a href="#/try-on">Try something on</a>.</p>}
      <div className="grid wide">
        {rows?.map((r) => <figure key={r.id}><img src={r.image_url} alt={`${r.category} try-on`} loading="lazy" /><figcaption>{r.jewelry_id}</figcaption></figure>)}
      </div>
    </main>
  )
}
