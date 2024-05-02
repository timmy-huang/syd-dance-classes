const getData = async () => {
    // get data from the data folder
    try {
      const response = await fetch("../../data/mn-hurstville.json");
      if (!response.ok) {
        throw new Error('MN Hurstville data not found.');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Could not fetch data:", error);
      return null; // or handle the error as you prefer
    }
}

export default getData;