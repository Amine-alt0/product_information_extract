import { useState } from 'react'
import { checkcancel, searchEquipment } from './api/equipmentApi'
import AppLayout from './components/layout/AppLayout'
import ResearchInputPage from './components/input/ResearchInputPage'
import ResultsPage from './components/output/ResultsPage'
import HistoryPage from './components/history/HistoryPage'
import SettingsPage from './components/settings/SettingsPage'
import { computeConfidence, parseEquipmentMeta } from './utils/formatters'
import './App.css'

let historyIdCounter = 0

export default function App() {
  const [activeNav, setActiveNav] = useState('research')
  const [view, setView] = useState('input')
  const [equipmentName, setEquipmentName] = useState('')
  const [result, setResult] = useState(null)
  const [sessionHistory, setSessionHistory] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [themeIsLight, setThemeIsLight] = useState(true)
  const [requestId,setRequestId] = useState(null)
  async function handleSearch(name, hint) {
    setError('')
    setIsLoading(true)
    const id=crypto.randomUUID()
    setRequestId(id)
    try {
      const data = await searchEquipment(name, hint,id)
      const entry = {
        id: ++historyIdCounter,
        equipmentName: name,
        hint: hint || '',
        result: data,
        searchedAt: new Date().toISOString(),
      }

      setEquipmentName(name)
      setResult(data)
      setSessionHistory((current) => [entry, ...current])
      setView('results')
      setActiveNav('research')
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  function handleBack() {
    setView('input')
    setError('')
    setActiveNav('research')
  }

  function handleNavSelect(navId) {
    if (navId === 'reports') return

    setActiveNav(navId)
    setError('')

    if (navId === 'research') {
      setView('input')
      return
    }

    if (navId === 'history') {
      setView('history')
      return
    }

    if (navId === 'settings') {
      setView('settings')
    }
  }

  function handleOpenHistoryEntry(entry) {
    setEquipmentName(entry.equipmentName)
    setResult(entry.result)
    setView('results')
    setActiveNav('research')
  }

  const meta = result ? parseEquipmentMeta(equipmentName, result) : null
  const confidence = result ? computeConfidence(result) : 0
  function handleCancel(){
    if (requestId) {
      checkcancel(requestId);
    }
  }
  function renderMain() {
    if (view === 'results' && result) {
      return (
        <ResultsPage
          result={result}
          meta={meta}
          confidence={confidence}
          onBack={handleBack}
        />
      )
    }

    if (view === 'history') {
      return (
        <HistoryPage
          items={sessionHistory}
          onOpen={handleOpenHistoryEntry}
          onNewResearch={() => handleNavSelect('research')}
        />
      )
    }

    if (view === 'settings') {
      return (
        <SettingsPage
          themeIsLight={themeIsLight}
          onToggleTheme={() => setThemeIsLight((light) => !light)}
        />
      )
    }

    return (
      <ResearchInputPage onSubmit={handleSearch} oncancel={handleCancel} isLoading={isLoading} error={error} />
    )
  }

  return (
    <AppLayout
      activeNav={activeNav}
      onNavSelect={handleNavSelect}
      themeIsLight={themeIsLight}
      onThemeChange={setThemeIsLight}
    >
      {renderMain()}
    </AppLayout>
  )
}
