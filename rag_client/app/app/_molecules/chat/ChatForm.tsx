"use client";

import { FormEvent, useContext, useEffect, useState } from "react";

import { z } from "zod";

import { ChatContext } from "@/app/_context/chatContext";
import { getClientAskChat } from "@/app/_models/chat";
import Button from "@/app/_atoms/button/Button";
import Spinner from "@/app/_atoms/spinner/Spinner";
import Textarea from "@/app/_atoms/textarea/Textarea";
import Select, { Option } from "@/app/_molecules/select/Select";
import { ChatMode } from "@/app/types";

const contentSchema = z
  .string()
  .min(2, { message: "👉 min 2 characters" })
  .max(1000, { message: "👉 max 1000 characters" });

const options: Option<ChatMode>[] = [
  {
    label: "Chat",
    value: "chat",
  },
  {
    label: "RAG",
    value: "rag",
  },
];

const LoginForm = ({ id }: { id: string }) => {
  const [content, setContent] = useState("");
  const [chatMode, setChatMode] = useState<ChatMode>(options[0].value);
  const [errors, setErrors] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { setQuestions } = useContext(ChatContext);

  const cleanContent = content.trim();
  const isError = errors.length > 0;

  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (isError) {
      return;
    }
    setIsLoading(true);
    try {
      const res = await getClientAskChat(id, content, chatMode);
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

  useEffect(() => {
    try {
      contentSchema.parse(cleanContent);
      setErrors([]);
    } catch (error) {
      if (error instanceof z.ZodError) {
        setErrors(error.errors.map((e) => e.message));
      }
    }
  }, [cleanContent]);

  return (
    <form className="space-y-5" onSubmit={onSubmitHandler}>
      <Select<ChatMode>
        options={options}
        onOptionChange={(o) => {
          setChatMode(o.value);
        }}
        defaultOption={options[0]}
        label="Select mode"
      />
      <div className="relative">
        {isLoading && <Spinner className="absolute-center" />}
        <label>
          <small className="text-red">{errors.join("\n")}</small>
          <Textarea
            value={content}
            placeholder="Write your question here..."
            onChange={(e) => setContent(e.target.value)}
            disabled={isLoading}
          />
        </label>
      </div>
      <div className="flex justify-end">
        <Button type="submit" disabled={isLoading || isError}>
          Ask {chatMode}
        </Button>
      </div>
    </form>
  );
};

export default LoginForm;
