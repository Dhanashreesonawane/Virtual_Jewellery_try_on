export const MAX_FILE_MB = 8
export const ALLOWED = ['image/jpeg', 'image/png']

export function validateFile(file) {
  if (!file) return 'Choose an image first.'
  if (!ALLOWED.includes(file.type)) return 'Please use a JPG or PNG image.'
  if (file.size > MAX_FILE_MB * 1024 * 1024) return `Image must be under ${MAX_FILE_MB} MB.`
  return null
}

// Downscale + re-encode as JPEG before upload (faster, smaller requests).
export function compressImage(file, maxSide = 1280, quality = 0.9) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file)
    const img = new Image()
    img.onload = () => {
      const s = Math.min(1, maxSide / Math.max(img.width, img.height))
      const c = document.createElement('canvas')
      c.width = Math.round(img.width * s); c.height = Math.round(img.height * s)
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height)
      URL.revokeObjectURL(url)
      c.toBlob((b) => (b ? resolve(b) : reject(new Error('compress'))), 'image/jpeg', quality)
    }
    img.onerror = () => { URL.revokeObjectURL(url); reject(new Error('Image could not be read.')) }
    img.src = url
  })
}

export async function downloadImage(url, name = 'tryon-result.jpg') {
  const blob = await (await fetch(url)).blob()
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob); a.download = name; a.click()
  setTimeout(() => URL.revokeObjectURL(a.href), 1000)
}

export async function shareImage(url) {
  const blob = await (await fetch(url)).blob()
  const file = new File([blob], 'tryon-result.jpg', { type: 'image/jpeg' })
  if (navigator.canShare?.({ files: [file] })) {
    await navigator.share({ files: [file], title: 'My jewellery try-on' })
    return 'shared'
  }
  return 'unsupported'
}
