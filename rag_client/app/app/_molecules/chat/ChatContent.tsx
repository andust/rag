"use client";

import { useContext, useEffect } from "react";

import { ChatContext } from "@/app/_context/chatContext";
import { Chat, getClientChat } from "@/app/_models/chat";

const ChatContent = ({ id }: { id: string }) => {
  const { questions, setQuestions } = useContext(ChatContext);
  useEffect(() => {
    getClientChat(id)
      .then((res) => {
        return res.json();
      })
      .then((chat: Chat) => {
        setQuestions(chat.questions);
      });
  }, [id, setQuestions]);

  return (
    <div className="space-y-8">
      {questions?.map((question, index) => (
        <div key={`${question.content}-${index}`}>
          <h2 className="p-2 rounded bg-slate-700 mb-1">{question.content}</h2>
          <p className="p-2 text-right w-4/5 bg-slate-900 rounded ml-auto mr-0">
            {question.answer}
          </p>
        </div>
      ))}
    </div>
  );
};

export default ChatContent;
