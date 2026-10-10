// All backend calls live here. The adapter unwraps {success,data,error} envelopes.
const BASE = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

export class ApiError extends Error {
  constructor(code, message) { super(message); this.code = code }
}

export const assetUrl = (path) => (path ? `${BASE}${path.startsWith('/') ? '' : '/'}${path}` : '')

async function request(path, options) {
  let res
  try { res = await fetch(`${BASE}${path}`, options) }
  catch { throw new ApiError('BACKEND_UNAVAILABLE', 'Cannot reach the try-on server.') }
  let body = null
  try { body = await res.json() } catch { /* non-JSON error */ }
  if (!body || !body.success) {
    throw new ApiError(body?.error?.code || 'PROCESSING_FAILED', body?.error?.message || 'Request failed.')
  }
  return body.data
}

const withUrls = (d) => ({ ...d, image_url: assetUrl(d.image_url) })
const json = (payload) => ({ method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })

export const healthCheck = () => request('/api/health')
export const getJewelry = async (category) => {
  const items = await request(`/api/jewelry${category ? `?category=${category}` : ''}`)
  return items.map((i) => ({ ...i, thumbnail_url: assetUrl(i.thumbnail_url) }))
}
export const getJewelryById = (id) => request(`/api/jewelry/${encodeURIComponent(id)}`)

export async function tryOnImage(file, jewelryId, category, side = 'both') {
  const form = new FormData()
  form.append('image', file, 'photo.jpg')
  form.append('jewelry_id', jewelryId)
  form.append('category', category)
  form.append('side', side)
  return withUrls(await request('/api/tryon/image', { method: 'POST', body: form }))
}
export async function tryOnFrame(frameDataUrl, jewelryId, category, side = 'both') {
  return withUrls(await request('/api/tryon/frame',
    json({ image: frameDataUrl, jewelry_id: jewelryId, category, side })))
}
export async function saveResult(r) {
  // The backend only accepts its own /outputs/ paths, so strip the base URL.
  return request('/api/results', json({
    image_url: r.image_url.replace(BASE, ''), jewelry_id: r.jewelry_id,
    category: r.category, processing_time_ms: r.processing_time_ms,
  }))
}
export async function getResults() {
  const rows = await request('/api/results')
  return rows.map((r) => ({ ...r, image_url: assetUrl(r.image_url) }))
}

// WebSocket URL for live try-on, derived from the same base URL.
export const wsUrl = () => `${BASE.replace(/^http/, 'ws')}/ws/tryon`
