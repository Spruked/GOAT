import { useState } from 'react'
import { useQuery, useMutation } from '@tantml:react-query'
import { GraduationCap, BookOpen, Award } from 'lucide-react'
import axios from 'axios'

export function TeacherPage() {
  const [userId] = useState('user_demo')
  const [currentQuiz, setCurrentQuiz] = useState(null)
  const [answers, setAnswers] = useState({})
  const [quizResult, setQuizResult] = useState(null)

  const { data: recommendation } = useQuery({
    queryKey: ['recommendation', userId],
    queryFn: async () => {
      const { data } = await axios.get(`/api/teach/recommend/${userId}`)
      return data
    }
  })

  const generateQuiz = useMutation({
    mutationFn: async (skillId) => {
      const { data } = await axios.get(`/api/teach/quiz/${skillId}`)
      return data
    },
    onSuccess: (data) => {
      setCurrentQuiz(data)
      setAnswers({})
      setQuizResult(null)
    }
  })

  const submitQuiz = useMutation({
    mutationFn: async () => {
      const { data } = await axios.post('/api/teach/submit-quiz', {
        quiz_id: currentQuiz.skill_id,
        answers
      })
      return data
    },
    onSuccess: (data) => {
      setQuizResult(data)
    }
  })

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Adaptive Learning</h1>
        <p className="text-slate-400">
          AI-powered personalized learning paths
        </p>
      </div>

      {/* Recommendation */}
      {recommendation && !recommendation.completed_all && (
        <div className="goat-card">
          <div className="flex items-center gap-3 mb-4">
            <BookOpen className="w-6 h-6 text-goat-primary" />
            <h2 className="text-2xl font-bold">Recommended for You</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-semibold">
                {recommendation.skill?.name}
              </h3>
              <p className="text-slate-400 text-sm">
                {recommendation.skill?.description}
              </p>
              <div className="flex gap-2 mt-2">
                <span className="px-2 py-1 bg-slate-700 rounded text-xs">
                  {recommendation.skill?.difficulty}
                </span>
                <span className="px-2 py-1 bg-slate-700 rounded text-xs">
                  {recommendation.skill?.category}
                </span>
              </div>
            </div>

            {recommendation.teaching_nfts?.length > 0 && (
              <div>
                <h4 className="font-semibold mb-2">Learning Resources</h4>
                <div className="space-y-2">
                  {recommendation.teaching_nfts.map((nft, idx) => (
                    <div key={idx} className="bg-slate-700 rounded p-3 flex items-center gap-3">
                      <img 
                        src={`/glyph/svg/${nft.glyph_id}`} 
                        alt="Glyph" 
                        className="w-10 h-10 rounded"
                      />
                      <div className="flex-1">
                        <div className="font-medium">{nft.title}</div>
                        <div className="text-xs text-slate-400">
                          Confidence: {Math.round(nft.confidence * 100)}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={() => generateQuiz.mutate(recommendation.skill.id)}
              className="goat-button w-full"
              disabled={generateQuiz.isPending}
            >
              {generateQuiz.isPending ? 'Generating Quiz...' : 'Start Quiz'}
            </button>
          </div>
        </div>
      )}

      {/* Quiz */}
      {currentQuiz && !quizResult && (
        <div className="goat-card">
          <div className="flex items-center gap-3 mb-4">
            <GraduationCap className="w-6 h-6 text-goat-primary" />
            <h2 className="text-2xl font-bold">Quiz: {currentQuiz.skill_id}</h2>
          </div>

          <div className="space-y-6">
            {currentQuiz.questions?.map((question, idx) => (
              <div key={question.id} className="bg-slate-700 rounded-lg p-4">
                <h4 className="font-semibold mb-3">
                  {idx + 1}. {question.question}
                </h4>
                <div className="space-y-2">
                  {question.options?.map((option, optIdx) => {
                    const letter = String.fromCharCode(65 + optIdx)
                    return (
                      <label
                        key={optIdx}
                        className="flex items-center gap-3 p-3 bg-slate-800 rounded cursor-pointer hover:bg-slate-600 transition"
                      >
                        <input
                          type="radio"
                          name={question.id}
                          value={letter}
                          checked={answers[question.id] === letter}
                          onChange={(e) => setAnswers({...answers, [question.id]: e.target.value})}
                          className="w-4 h-4"
                        />
                        <span>{letter}. {option}</span>
                      </label>
                    )
                  })}
                </div>
              </div>
            ))}

            <button
              onClick={() => submitQuiz.mutate()}
              disabled={Object.keys(answers).length < currentQuiz.questions.length}
              className="goat-button w-full disabled:opacity-50"
            >
              Submit Quiz
            </button>
          </div>
        </div>
      )}

      {/* Quiz Result */}
      {quizResult && (
        <div className={`goat-card ${quizResult.passed ? 'bg-green-900 bg-opacity-20 border-green-500' : 'bg-red-900 bg-opacity-20 border-red-500'}`}>
          <div className="flex items-center gap-3 mb-4">
            <Award className={`w-6 h-6 ${quizResult.passed ? 'text-green-500' : 'text-red-500'}`} />
            <h2 className="text-2xl font-bold">
              {quizResult.passed ? 'Congratulations!' : 'Keep Learning!'}
            </h2>
          </div>

          <div className="space-y-4">
            <div className="text-center">
              <div className="text-4xl font-bold mb-2">
                {Math.round(quizResult.score * 100)}%
              </div>
              <div className="text-slate-400">
                {quizResult.correct_count} / {quizResult.total_questions} correct
              </div>
            </div>

            {quizResult.passed && (
              <button className="goat-button w-full">
                Mint Learner Badge
              </button>
            )}

            <button
              onClick={() => {
                setCurrentQuiz(null)
                setQuizResult(null)
                setAnswers({})
              }}
              className="goat-button-secondary w-full"
            >
              Try Another Skill
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
