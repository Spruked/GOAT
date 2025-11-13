import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { User, Award, TrendingUp } from 'lucide-react'
import axios from 'axios'

export function ProfilePage() {
  const { userId } = useParams()

  const { data: progress } = useQuery({
    queryKey: ['progress', userId],
    queryFn: async () => {
      const { data } = await axios.get(`/api/teach/progress/${userId}`)
      return data
    }
  })

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="goat-card">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-gradient-to-r from-goat-primary to-goat-secondary rounded-full flex items-center justify-center">
            <User className="w-8 h-8 text-slate-900" />
          </div>
          <div>
            <h1 className="text-3xl font-bold">{userId}</h1>
            <p className="text-slate-400">Learner Profile</p>
          </div>
        </div>
      </div>

      {progress && (
        <>
          {/* Stats */}
          <div className="grid grid-cols-3 gap-4">
            <StatCard
              icon={<Award className="w-6 h-6" />}
              label="Skills Mastered"
              value={progress.total_skills}
              color="from-blue-500 to-cyan-500"
            />
            <StatCard
              icon={<TrendingUp className="w-6 h-6" />}
              label="Average Mastery"
              value={`${Math.round(progress.average_mastery * 100)}%`}
              color="from-green-500 to-emerald-500"
            />
            <StatCard
              icon={<Award className="w-6 h-6" />}
              label="Badges Earned"
              value={progress.mastered_skills?.filter(s => s.mastery_level >= 0.7).length || 0}
              color="from-purple-500 to-pink-500"
            />
          </div>

          {/* Mastered Skills */}
          <div className="goat-card">
            <h2 className="text-2xl font-bold mb-4">Mastered Skills</h2>
            <div className="space-y-3">
              {progress.mastered_skills?.map((skill, idx) => (
                <div key={idx} className="bg-slate-700 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold">{skill.name}</h3>
                    <span className="text-goat-primary font-bold">
                      {Math.round(skill.mastery_level * 100)}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-600 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-goat-primary to-goat-secondary h-2 rounded-full transition-all"
                      style={{ width: `${skill.mastery_level * 100}%` }}
                    />
                  </div>
                  <div className="text-xs text-slate-400 mt-2">
                    Last practiced: {new Date(skill.last_practiced).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}

function StatCard({ icon, label, value, color }) {
  return (
    <div className="goat-card">
      <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${color} flex items-center justify-center mb-3`}>
        {icon}
      </div>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-sm text-slate-400">{label}</div>
    </div>
  )
}
