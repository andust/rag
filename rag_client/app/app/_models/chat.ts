export interface Chat {
  id: string;
  questions: Question[];
}

export interface Question {
  content: string;
  answer: string;
}

export const getClientChat = async (id: string) => {
  return fetch(`${process.env.NEXT_PUBLIC_CHAT_SERIVCE}/api/v1/chat/${id}`, {
    cache: "no-cache",
    credentials: "include",
    method: "get",
  });
};

export const getClientAskChat = async (id: string, question: string) => {
  return fetch(
    `${process.env.NEXT_PUBLIC_CHAT_SERIVCE}/api/v1/chat/ask/${id}`,
    {
      cache: "no-cache",
      credentials: "include",
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content: question }),
    }
  );
};

export const removeClientChat = async (id: string) => {
  return fetch(`${process.env.NEXT_PUBLIC_CHAT_SERIVCE}/api/v1/chat/${id}`, {
    cache: "no-cache",
    credentials: "include",
    method: "delete",
  });
};
