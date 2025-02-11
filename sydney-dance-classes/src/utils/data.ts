import { Lesson } from './types';
import { Ref } from 'vue';
import { studios } from './consts';

const getData = async (lessons: Ref<Lesson[]>) => {
  // get data from the data folder

  studios.forEach(async (file) => {
    try {
      const response = await fetch(`data/${file}.json`);
      if (!response.ok) {
        throw new Error('Data not found.');
      }
      const data = await response.json();
      data.forEach((lesson: Lesson) => {
        lessons.value.push({
          ...lesson,
          start: new Date(lesson.start),
          end: new Date(lesson.end),
          studio: file.replace('.json', ''),
          level: determineLevel(lesson.name)
        });
      });
    } catch (error) {
      console.error(`Could not fetch data for ${file}:`, error);
    }
  });
  console.log('lessons');
  console.log(lessons);
  return lessons;
}

const determineLevel = (name: string): string[] => {
  if (name.toLowerCase().includes('int/adv')) {
    return ['intermediate', 'advanced'];
  } else if (name.toLowerCase().includes('beginner')) {
    return ['beginner'];
  } else if (name.toLowerCase().includes('intermediate')) {
    return ['intermediate'];
  } else {
    return ['advanced'];
  }
}

export default getData;