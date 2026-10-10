export default function Home() {
  return (
    <main>
      <section className="hero">
        <div>
          <h1>Try jewellery virtually before you buy</h1>
          <p>Use your camera or upload a photo. We find your hand, ears or shoulders and place rings, bangles, earrings and necklaces on you.</p>
          <div className="row">
            <a className="btn" href="#/try-on">Try it now</a>
            <a className="btn ghost" href="#/try-on?mode=upload">Upload photo</a>
          </div>
        </div>
        <div className="preview" aria-hidden="true">
          <svg viewBox="0 0 200 200"><circle cx="100" cy="120" r="56" fill="none" stroke="var(--gold)" strokeWidth="9" /><path d="M78 60 100 30 122 60 100 82Z" fill="#9ec3de" stroke="var(--gold)" strokeWidth="5" /></svg>
          <span>Your photo, with the piece you choose.</span>
        </div>
      </section>
      <section id="about" className="about">
        <h2>About</h2>
        <p>Aurelia is a BE Electronics &amp; Telecommunication project. A Python backend uses MediaPipe landmark detection, geometric alignment and alpha compositing; this site only handles input and display.</p>
      </section>
    </main>
  )
}
