import {

  HistoryIcon,

  LogoIcon,

  PlusIcon,

  ReportIcon,

  SettingsIcon,

} from '../icons/Icons'



const NAV_ITEMS = [

  { id: 'research', label: 'New Research', icon: PlusIcon },

  { id: 'history', label: 'History', icon: HistoryIcon },

  { id: 'reports', label: 'Reports', icon: ReportIcon, disabled: true },

  { id: 'settings', label: 'Settings', icon: SettingsIcon },

]



export default function Sidebar({ mobileOpen, onClose, activeNav, onNavSelect }) {

  return (

    <>

      <div

        className={`sidebar-overlay ${mobileOpen ? 'visible' : ''}`}

        onClick={onClose}

        aria-hidden="true"

      />

      <aside className={`sidebar ${mobileOpen ? 'open' : ''}`}>

        <div className="sidebar-brand">

          <LogoIcon />

          <div>

            <strong>Equipment Intelligence</strong>

          </div>

        </div>



        <nav className="sidebar-nav" aria-label="Main">

          {NAV_ITEMS.map(({ id, label, icon: Icon, disabled }) => (

            <button

              key={id}

              type="button"

              className={`nav-item ${activeNav === id ? 'active' : ''}`}

              disabled={disabled}

              aria-current={activeNav === id ? 'page' : undefined}

              onClick={() => onNavSelect?.(id)}

            >

              <Icon />

              <span>{label}</span>

            </button>

          ))}

        </nav>



        <div className="sidebar-status">

          <span className="status-dot" />

          <div>

            <strong>System ready</strong>

            <p>AI-powered equipment research for your inspections</p>

          </div>

        </div>

      </aside>

    </>

  )

}

