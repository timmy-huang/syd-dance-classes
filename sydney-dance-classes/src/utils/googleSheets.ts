/**
 * Fetches data from a public Google Spreadsheet
 * @param spreadsheetId The ID of the Google Spreadsheet
 * @param sheetName The name of the sheet to fetch
 * @returns The values from the spreadsheet
 */
export const fetchSheetData = async (spreadsheetId: string, sheetName: string) => {
  try {
    const response = await fetch(
      `https://docs.google.com/spreadsheets/d/${spreadsheetId}/gviz/tq?tqx=out:json&sheet=${sheetName}`
    )

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const text = await response.text()
    // Remove the "google.visualization.Query.setResponse(" from the start and ");" from the end
    const jsonText = text.substring(47, text.length - 2)
    const data = JSON.parse(jsonText)

    // Transform the data into a simple array of arrays
    return data.table.rows.map((row: any) => {
      const values = row.c.map((cell: any) => {
        if (!cell) return ''
        // Handle date format
        if (typeof cell.v === 'string' && cell.v.startsWith('Date(')) {
          // Extract date parts from "Date(year,month,day,hour,minute,second)"
          const dateStr = cell.v.replace('Date(', '').replace(')', '')
          const [year, month, day, hour, minute, second] = dateStr.split(',').map(Number)
          return new Date(year, month, day, hour, minute, second)
        }
        return cell.v ?? ''
      })
      return values
    })
  } catch (error) {
    console.error('Error fetching sheet data:', error)
    throw error
  }
} 