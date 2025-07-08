import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';

interface VoterResult {
  name: string;
  choice1: number;
  choice2: number;
  choice3: number;
  assigned_land: number | null;
}

export default function ResultsPage() {
  const router = useRouter();
  const { round } = router.query;
  const [results, setResults] = useState<VoterResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (round) {
      const fetchResults = async () => {
        try {
          const response = await fetch(`http://localhost:8000/draft/${round}`);
          if (!response.ok) {
            throw new Error(`エラー: ${response.statusText}`);
          }
          const data: VoterResult[] = await response.json();
          setResults(data);
        } catch (err: any) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      };
      fetchResults();
    }
  }, [round]);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-xl">結果を読み込み中...</div>;
  }

  if (error) {
    return <div className="min-h-screen flex items-center justify-center text-red-500 text-xl">エラー: {error}</div>;
  }

  return (
    <div className="min-h-screen p-8 flex flex-col items-center">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md w-full">
        <h1 className="text-3xl font-extrabold mb-8 text-center text-gray-900">ラウンド{round} 結果</h1>
        {
          results.length === 0 ? (
            <p className="text-center text-gray-600 text-lg">このラウンドの結果はまだありません。</p>
          ) : (
            <div className="overflow-x-auto bg-white rounded-lg shadow-lg p-4">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="py-3 px-6 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">投票者名</th>
                    <th className="py-3 px-6 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">第1希望候補地</th>
                    {round !== '1' && (
                      <th className="py-3 px-6 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">第2希望候補地</th>
                    )}
                    {round !== '1' && round !== '2' && (
                      <th className="py-3 px-6 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">第3希望候補地</th>
                    )}
                    <th className="py-3 px-6 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">割り当てられた土地</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {results.map((voter, index) => (
                    <tr key={index} className="hover:bg-gray-50 transition duration-150 ease-in-out">
                      <td className="py-3 px-6 whitespace-nowrap text-sm font-medium text-gray-900">{voter.name}</td>
                      <td className="py-3 px-6 whitespace-nowrap text-sm text-gray-700">{voter.choice1}</td>
                      {round !== '1' && (
                        <td className="py-3 px-6 whitespace-nowrap text-sm text-gray-700">{voter.choice2}</td>
                      )}
                      {round !== '1' && round !== '2' && (
                        <td className="py-3 px-6 whitespace-nowrap text-sm text-gray-700">{voter.choice3}</td>
                      )}
                      <td className="py-3 px-6 whitespace-nowrap text-sm font-semibold ${voter.assigned_land !== null ? 'text-green-600' : 'text-red-500'}">
                        {voter.assigned_land !== null ? voter.assigned_land : '未割り当て'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )
        }
        <div className="mt-10 flex justify-center space-x-6">
          {round && parseInt(round as string) < 4 && (
            <button
              onClick={() => router.push(`/results/${parseInt(round as string) + 1}`)}
              className="py-3 px-8 bg-indigo-600 text-white font-bold rounded-full shadow-lg hover:bg-indigo-700 transform hover:scale-105 transition duration-300 ease-in-out"
            >
              ラウンド{parseInt(round as string) + 1}へ進む
            </button>
          )}
          {round && parseInt(round as string) > 1 && (
            <button
              onClick={() => router.push(`/results/${parseInt(round as string) - 1}`)}
              className="py-3 px-8 bg-gray-300 text-gray-800 font-bold rounded-full shadow-lg hover:bg-gray-400 transform hover:scale-105 transition duration-300 ease-in-out"
            >
              ラウンド{parseInt(round as string) - 1}に戻る
            </button>
          )}
        </div>
      </div>
    </div>
  );
}