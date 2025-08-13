'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [choice1, setChoice1] = useState('');
  const [choice2, setChoice2] = useState('');
  const [choice3, setChoice3] = useState('');
  const [votersCount, setVotersCount] = useState(0);

  useEffect(() => {
    const fetchVotersCount = async () => {
      try {
        const response = await fetch('http://localhost:8000/voters/count');
        if (response.ok) {
          const count = await response.json();
          setVotersCount(count);
        }
      } catch (error) {
        console.error('Failed to fetch voters count:', error);
      }
    };

    fetchVotersCount();
    const interval = setInterval(fetchVotersCount, 5000); // 5秒ごとに更新
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/voters', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          choice1: parseInt(choice1),
          choice2: parseInt(choice2),
          choice3: parseInt(choice3),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '投票者の登録に失敗しました');
      }

      alert('投票者の登録が完了しました！');
      setName('');
      setChoice1('');
      setChoice2('');
      setChoice3('');
      // 投票者数も更新
      const updatedCountResponse = await fetch('http://localhost:8000/voters/count');
      if (updatedCountResponse.ok) {
        const updatedCount = await updatedCountResponse.json();
        setVotersCount(updatedCount);
      }
    } catch (error: any) {
      alert(error.message);
    }
  };

  const handleRunDraft = async () => {
    try {
      const response = await fetch('http://localhost:8000/draft/run', {
        method: 'POST',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'ドラフトの実行に失敗しました');
      }

      alert('ドラフトの実行が完了しました！');
      router.push('/results/1'); // Redirect to round 1 results
    } catch (error: any) {
      alert(error.message);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md mb-8">
        <h1 className="text-2xl font-bold mb-6 text-center">XANA DAO Village 土地抽選会</h1>
        <div className="text-center mb-4">
          <Link href="/voters" className="text-indigo-600 hover:text-indigo-800 font-medium">
            投票完了者一覧を見る
          </Link>
        </div>
        <p className="text-center text-lg mb-4">現在の登録者数: {votersCount} / 23</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">投票者名（ニックネーム）</label>
            <input
              type="text"
              id="name"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="choice1" className="block text-sm font-medium text-gray-700">第1希望候補地 (1-32)</label>
            <input
              type="number"
              id="choice1"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              value={choice1}
              onChange={(e) => setChoice1(e.target.value)}
              min="1"
              max="32"
              required
            />
          </div>
          <div>
            <label htmlFor="choice2" className="block text-sm font-medium text-gray-700">第2希望候補地 (1-32)</label>
            <input
              type="number"
              id="choice2"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              value={choice2}
              onChange={(e) => setChoice2(e.target.value)}
              min="1"
              max="32"
              required
            />
          </div>
          <div>
            <label htmlFor="choice3" className="block text-sm font-medium text-gray-700">第3希望候補地 (1-32)</label>
            <input
              type="number"
              id="choice3"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              value={choice3}
              onChange={(e) => setChoice3(e.target.value)}
              min="1"
              max="32"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            投票者を登録する
          </button>
        </form>
      </div>

      {votersCount >= 10 && (
        <button
          onClick={handleRunDraft}
          className="mt-4 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          ドラフトを実行してラウンド1の結果を見る
        </button>
      )}
    </div>
  );
}