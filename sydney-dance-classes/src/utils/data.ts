import { Lesson } from './types';
import { Ref } from 'vue';

const fileList = [
  "mn-hurstville.json",
  "mn-parramatta.json",
]

const getData = async (lessons: Ref<Lesson[]>) => {
    // get data from the data folder

    fileList.forEach(async (file) => {
      try {
        const response = await fetch(`../../data/${file}`);
        if (!response.ok) {
          throw new Error('Data not found.');
        }
        const data = await response.json();
        data.forEach((lesson: Lesson) => {
            lessons.value.push({
              ...lesson,
              start: new Date(lesson.start),
              end: new Date(lesson.end)
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

export default getData;