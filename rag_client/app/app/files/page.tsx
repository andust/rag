import Link from "next/link";
import MainLayout from "@/app/_layout/MainLayout";
import { cookies } from "next/headers";
import { getFiles } from "../_utils/fetch/file";
import { DocFile } from "../_models/file";

export default async function New() {
  let files: DocFile[] = [];
  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    const res = await getFiles(access);
    if (res.ok) {
      files = await res.json();
    }
  } catch (error) {
    console.log(error);
  }
  return (
    <MainLayout>
      <Link href="/files/upload">Upload files</Link>
      {files.map(({ id, filename }) => (
        <p key={id}>{filename}</p>
      ))}
    </MainLayout>
  );
}
