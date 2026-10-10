const links = [['#/', 'Home'], ['#/try-on', 'Virtual Try-On'], ['#/try-on', 'Jewelry Collection'], ['#/results', 'Saved looks']]
export default function Header({ route }) {
  return (
    <header className="header">
      <a className="logo" href="#/" aria-label="Aurelia home">Aurelia</a>
      <nav aria-label="Main">
        {links.map(([href, label]) => (
          <a key={label} href={href} aria-current={route === href.slice(1) && label !== 'Jewelry Collection' ? 'page' : undefined}>{label}</a>
        ))}
        <a href="#about">About</a>
      </nav>
    </header>
  )
}
