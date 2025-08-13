'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

interface Voter {
  name: string;
  choice1: number;
  choice2: number;
  choice3: number;
}

export default function VotersPage() {
  const [voters, setVoters] = useState<Voter[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchVoters = async () => {
      try {
        const response = await fetch('http://localhost:8000/voters');
        if (!response.ok) {
          throw new Error('投票者リストの取得に失敗しました');
        }
        const data = await response.json();
        setVoters(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchVoters();
  }, []);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">読み込み中...</div>;
  }

  if (error) {
    return <div className="min-h-screen flex items-center justify-center text-red-500">エラー: {error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4 sm:p-8">
      <div className="w-full max-w-4xl bg-white p-6 sm:p-8 rounded-lg shadow-md">
        <h1 className="text-2xl sm:text-3xl font-bold mb-6 text-center text-gray-800">投票完了者一覧</h1>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  投票者名
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {voters.map((voter) => (
                <tr key={voter.name}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{voter.name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-6 text-center">
          <Link href="/" className="text-indigo-600 hover:text-indigo-800 font-medium">
            投票ページに戻る
          </Link>
        </div>
      </div>
    </div>
  );
}
