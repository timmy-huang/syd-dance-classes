// Studios are now fetched from the database via useStudios composable
// This is kept for backward compatibility but will be empty
// Components should use useStudios() composable instead
const studios: string[] = []

const styles = [
  "Hip Hop",
  "K-Pop",
  "Heels",
  "Contemporary",
  "Jazz",
  "Ballet",
  "Popping",
  "Locking",
  "Breaking",
  "Waacking",
  "House",
  "Afro",
  "Dancehall",
  "Reggaeton",
  "Commercial",
  "Girl Style",
  "Vogue",
  "Stretch / Conditioning",
  "Choreography",
  "Other"
]

export { studios, styles };
