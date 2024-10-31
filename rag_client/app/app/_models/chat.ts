export interface Chat {
  id: string;
  questions: Question[];
}

export interface Question {
    content: string;
    answer: string;
}
