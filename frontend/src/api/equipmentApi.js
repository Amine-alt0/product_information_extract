const API_BASE = import.meta.env.VITE_API_BASE_URL ?? ''
export async function checkcancel(request_id) {
  let response
  try {
    response = await fetch(`${API_BASE}/api/cancel/${request_id}`, {
      method: 'POST',
    })
  } catch {
    throw new Error(
      'Cannot reach the backend. Start it from the backend folder with: python debugger.py',
    )
  }
  let data
  try {
    data = await response.json()
  } catch {
    throw new Error('The backend returned an invalid response.')
  }

  if (!response.ok) {
    throw new Error(data.error || 'Research request failed. Please try again.')
  }

  return data
}
export async function searchEquipment(equipmentName, hint = '',id) {
  let response
  try {
    response = await fetch(`${API_BASE}/api/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        request_id: id.trim(),
        equipment_name: equipmentName.trim(),
        hint: hint.trim(),
      }),
    })
  } catch {
    throw new Error(
      'Cannot reach the backend. Start it from the backend folder with: python debugger.py',
    )
  }

  let data
  try {
    data = await response.json()
  } catch {
    throw new Error('The backend returned an invalid response.')
  }

  if (!response.ok) {
    throw new Error(data.error || 'Research request failed. Please try again.')
  }

  return data
}
