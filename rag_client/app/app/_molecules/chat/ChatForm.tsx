"use client";

import { FormEvent, useContext, useState } from "react";

import Button from "@/app/_atoms/button/Button";
import { ChatContext } from "@/app/_context/chatContext";
import { getClientAskChat } from "@/app/_models/chat";

const LoginForm = ({ id }: { id: string }) => {
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { setQuestions } = useContext(ChatContext);

  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await getClientAskChat(id, content);
      if (res.ok) {
        const resData = await res.json();
        setQuestions(resData);
        setContent("");
      }
    } catch (err) {
      console.log(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="space-y-5 text-black" onSubmit={onSubmitHandler}>
      <label>
        <textarea
          rows={4}
          placeholder="Write your question here..."
          onChange={(e) => setContent(e.target.value)}
          value={content}
        ></textarea>
      </label>
      <div className="flex justify-end">
        <Button type="submit" disabled={isLoading}>
          Ask
        </Button>
      </div>
    </form>
  );
};

export default LoginForm;
