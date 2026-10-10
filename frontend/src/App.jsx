import { useEffect, useState } from 'react'
import Header from './components/Header'
import Home from './pages/Home'
import Results from './pages/Results'
import TryOn from './pages/TryOn'

const path = () => (location.hash.replace(/^#/, '').split('?')[0] || '/')
export default function App() {
  const [route, setRoute] = useState(path())
  useEffect(() => {
    const on = () => setRoute(path())
    addEventListener('hashchange', on)
    return () => removeEventListener('hashchange', on)
  }, [])
  const Page = { '/try-on': TryOn, '/results': Results }[route] || Home
  return (<><Header route={route} /><Page key={location.hash} /></>)
}
