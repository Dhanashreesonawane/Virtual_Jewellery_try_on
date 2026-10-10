import { memo } from 'react'
function JewelryCard({ item, selected, onSelect }) {
  return (
    <button className={selected ? 'card on' : 'card'} aria-pressed={selected} onClick={() => onSelect(item.id)}>
      <span className="thumb"><img src={item.thumbnail_url} alt={item.name} loading="lazy" /></span>
      <span className="name">{item.name}</span>
      <span className="cat">{item.category}</span>
      <span className="pick">{selected ? 'Selected' : 'Try on'}</span>
    </button>
  )
}
export default memo(JewelryCard)
