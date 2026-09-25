import { useEffect, useState } from 'react'

import Header from './Header'

import Sidebar from './Sidebar'



export default function AppLayout({

  children,

  activeNav,

  onNavSelect,

  themeIsLight: themeIsLightProp,

  onThemeChange,

}) {

  const [mobileNavOpen, setMobileNavOpen] = useState(false)

  const [internalThemeLight, setInternalThemeLight] = useState(true)



  const themeIsLight = themeIsLightProp ?? internalThemeLight



  function toggleTheme() {

    const next = !themeIsLight

    if (onThemeChange) {

      onThemeChange(next)

    } else {

      setInternalThemeLight(next)

    }

  }



  useEffect(() => {

    document.documentElement.dataset.theme = themeIsLight ? 'light' : 'dark'

  }, [themeIsLight])



  function handleNavSelect(navId) {

    onNavSelect?.(navId)

    setMobileNavOpen(false)

  }



  return (

    <div className={`app-shell ${themeIsLight ? 'theme-light' : 'theme-dark'}`}>

      <Sidebar

        mobileOpen={mobileNavOpen}

        onClose={() => setMobileNavOpen(false)}

        activeNav={activeNav}

        onNavSelect={handleNavSelect}

      />

      <div className="app-main">

        <Header

          ontogglethemeClick={toggleTheme}

          theme={themeIsLight}

          showMenuButton

          onMenuClick={() => setMobileNavOpen((open) => !open)}

        />

        <main className="page-content">{children}</main>

      </div>

    </div>

  )

}

