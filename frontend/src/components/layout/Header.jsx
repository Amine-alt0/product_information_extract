import { LogoIcon, MenuIcon, SunIcon,SunIconDark } from '../icons/Icons'

export default function Header({ontogglethemeClick,theme,onMenuClick, showMenuButton = false }) {
  return (
    <header className="app-header">
      {showMenuButton && (
        <>
          <button type="button" className="icon-button mobile-only menu-button" onClick={onMenuClick} aria-label="Open menu">
            <MenuIcon />
          </button>
          <div className="mobile-brand mobile-only">
            
            <div>
              <strong>Equipment Intelligence</strong>
            </div>
          </div>
        </>
      )}

      <div className="header-spacer" />

      <div className="header-actions">
        <button
          type="button"
          className={`icon-button theme-toggle ${theme ? 'is-light' : 'is-dark'}`}
          aria-label={theme ? 'Switch to dark mode' : 'Switch to light mode'}
          aria-pressed={!theme}
          onClick={ontogglethemeClick}
        >
          {theme ? <SunIcon /> : <SunIconDark />}
        </button>
        <div className="user-profile">
          <div className="avatar">JD</div>
          <div className="user-meta desktop-only">
            <strong>RAMDANI Hacini </strong>
            <span>Inspector</span>
          </div>
        </div>
      </div>
    </header>
  )
}
