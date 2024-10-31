import { cookies } from "next/headers";
import MainLayout from "./_layout/MainLayout";
import { getChats } from "./_utils/fetch/chat";
import { Chat } from "./_models/chat";

export default async function Home() {
  let chats: Chat[] = [];
  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    const res = await getChats(access);
    if (res.ok) {
      chats = await res.json();
    }
  } catch (error) {
    console.log( error);
  }
  
  return (
    <MainLayout>
        Main page
        {chats.map(({ id, questions }) => <p key={id}>{questions[0].content} <br/>{questions[0].answer}</p>)}
    </MainLayout>
  );
}
