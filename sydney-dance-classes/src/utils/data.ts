import { Lesson } from './types';
import { Ref } from 'vue';
import { studios } from './consts';

const getData = async (lessons: Ref<Lesson[]>) => {
  try {
    const fetchPromises = studios.map(async (studioName) => {
      const file = studioName.replaceAll(' ', '_').toLowerCase();
      try {
        const response = await fetch(`${import.meta.env.BASE_URL}data/${file}.json`);
        if (!response.ok) {
          throw new Error('Data not found.');
        }
        const data = await response.json();
        data.forEach((lesson: Lesson) => {
          lessons.value.push({
            ...lesson,
            start: new Date(lesson.start),
            end: new Date(lesson.end),
            studio: studioName,
            choreo: {
              id: lesson.choreo.id || '',
              name: lesson.choreo.name || '',
              instagram: lesson.choreo.instagram || ''
            }
          });
        });
      } catch (error) {
        console.error(`Could not fetch data for ${file}:`, error);
      }
    });

    await Promise.all(fetchPromises);
    console.log('All data fetched, lessons count:', lessons.value.length);
    return lessons;
  } catch (error) {
    console.error('Error fetching data:', error);
    return lessons;
  }
}

export default getData;