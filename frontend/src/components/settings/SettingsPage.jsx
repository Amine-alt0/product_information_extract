export default function SettingsPage({ themeIsLight, onToggleTheme }) {
  return (
    <div className="settings-page">
      <section className="page-intro">
        <h1>Settings</h1>
        <p>Preferences for this session. Changes apply immediately.</p>
      </section>

      <section className="settings-panel">
        <article className="settings-card">
          <div className="settings-card-copy">
            <h2>Appearance</h2>
            <p>Switch between light and dark mode for the main workspace.</p>
          </div>
          <button
            type="button"
            className={`theme-switch ${themeIsLight ? 'is-light' : 'is-dark'}`}
            role="switch"
            aria-checked={!themeIsLight}
            onClick={onToggleTheme}
          >
            <span className="theme-switch-track">
              <span className="theme-switch-thumb" />
            </span>
            <span className="theme-switch-label">{themeIsLight ? 'Light mode' : 'Dark mode'}</span>
          </button>
        </article>

        <article className="settings-card">
          <div className="settings-card-copy">
            <h2>Session history</h2>
            <p>
              Research history is kept in memory while this tab is open. Refreshing the browser
              clears it.
            </p>
          </div>
        </article>
      </section>
    </div>
  )
}
