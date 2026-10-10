export const CATEGORIES = [['ring', 'Rings'], ['bangle', 'Bangles'], ['earring', 'Earrings'], ['necklace', 'Necklaces']]
export default function JewelryCategory({ value, onChange }) {
  return (
    <div className="tabs" role="tablist" aria-label="Jewellery category">
      {CATEGORIES.map(([id, label]) => (
        <button key={id} role="tab" aria-selected={value === id} className={value === id ? 'tab on' : 'tab'} onClick={() => onChange(id)}>{label}</button>
      ))}
    </div>
  )
}
