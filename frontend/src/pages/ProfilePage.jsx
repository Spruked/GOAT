import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { User, Award, TrendingUp, AlertTriangle } from 'lucide-react'
import axios from 'axios'

export function ProfilePage() {
  const { userId } = useParams()

  const { data: progress, isLoading, isError, error } = useQuery({
    queryKey: ['progress', userId],
    queryFn: async () => {
      const { data } = await axios.get(`/api/teach/progress/${userId}`)
      return data
    },
    enabled: !!userId
  })

  // Helper
  const formatDate = (d) =>
    d ? new Date(d).toLocaleDateString('en-US') : 'No data'

  if (!userId) {
    return (
      <div className="max-w-xl mx-auto goat-card text-center py-10">
        <AlertTriangle className="w-10 h-10 text-red-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-2">Invalid Profile</h2>
        <p className="text-slate-400">No user ID was provided.</p>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="text-center py-20">
        <p className="text-slate-400">Loading profile...</p>
      </div>
    )
  }

  if (isError) {
    return (
      <div className="max-w-xl mx-auto goat-card text-center py-10">
        <AlertTriangle className="w-10 h-10 text-red-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-2">Error Loading Profile</h2>
        <p className="text-slate-400">{error.message}</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
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

            {progress.mastered_skills?.length === 0 && (
              <p className="text-slate-400 text-sm">No mastered skills yet — keep going!</p>
            )}

            <div className="space-y-3">
              {progress.mastered_skills?.map((skill, idx) => {
                const percent = skill.mastery_level * 100

                const barColor =
                  percent >= 70
                    ? 'from-green-500 to-emerald-500'
                    : percent >= 40
                    ? 'from-yellow-500 to-amber-500'
                    : 'from-red-500 to-orange-500'

                return (
                  <div key={idx} className="bg-slate-700 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold">{skill.name}</h3>
                      <span className="font-bold text-goat-primary">
                        {Math.round(percent)}%
                      </span>
                    </div>

                    <div className="w-full bg-slate-600 rounded-full h-2 overflow-hidden">
                      <div
                        className={`bg-gradient-to-r ${barColor} h-2 rounded-full transition-all duration-700 ease-out`}
                        style={{ width: `${percent}%` }}
                      />
                    </div>

                    <div className="text-xs text-slate-400 mt-2">
                      Last practiced: {formatDate(skill.last_practiced)}
                    </div>
                  </div>
                )
              })}
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
