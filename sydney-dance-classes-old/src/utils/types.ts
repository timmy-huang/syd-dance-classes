// "serviceId": "06e3a68c-cc64-4587-be96-2cd77742543a",
//         "start": "2024-04-22T19:00:00.000+10:00",
//         "end": "2024-04-22T20:15:00.000+10:00",
//         "choreo": "Lana ",
//         "location": "390 Forest Road, Hurstville NSW, Australia",
//         "totalSpots": 25,
//         "openSpots": 21,
//         "name": "Int/Advanced Heels W Lana"

export type Lesson = {
    serviceId?: string;
    start: Date;
    end: Date;
    choreo: Choreographer;
    location?: string;
    totalSpots?: number;
    openSpots?: number;
    name: string;
    studio: string;
    level: string[];
    style: string[];
}

export type Choreographer = {
    id: string;
    name: string;
    instagram: string;
}