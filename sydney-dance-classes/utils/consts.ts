// Studios are now fetched from the database via useStudios composable
// This is kept for backward compatibility but will be empty
// Components should use useStudios() composable instead
const studios: string[] = []

const styles = [
  "Hip Hop",
  "Contemporary",
  "Choreography",
  "Kpop",
  "Heels",
  "Other"
]

export { studios, styles };