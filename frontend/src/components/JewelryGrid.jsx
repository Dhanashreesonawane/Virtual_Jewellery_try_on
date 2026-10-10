import JewelryCard from './JewelryCard'
export default function JewelryGrid({ items, selectedId, onSelect }) {
  if (!items.length) return <p className="muted">No jewellery available in this category yet.</p>
  return <div className="grid">{items.map((i) => <JewelryCard key={i.id} item={i} selected={i.id === selectedId} onSelect={onSelect} />)}</div>
}
