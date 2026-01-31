import React, { useState, useEffect } from 'react';
import { analyticsAPI, campaignsAPI, callsAPI } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalCampaigns: 0,
    activeCampaigns: 0,
    totalCalls: 0,
    completedCalls: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [overviewRes, campaignsRes, callsRes] = await Promise.all([
          analyticsAPI.getOverview(),
          campaignsAPI.getCampaigns(),
          callsAPI.getCalls()
        ]);

        const campaigns = campaignsRes.data;
        const calls = callsRes.data;

        setStats({
          totalCampaigns: campaigns.length,
          activeCampaigns: campaigns.filter(c => c.status === 'active').length,
          totalCalls: calls.length,
          completedCalls: calls.filter(c => c.status === 'completed').length
        });
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return <div className="container">Loading dashboard...</div>;
  }

  return (
    <div className="container">
      <h1>Dashboard</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card">
          <h3>Total Campaigns</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1976d2' }}>{stats.totalCampaigns}</p>
        </div>

        <div className="card">
          <h3>Active Campaigns</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#4caf50' }}>{stats.activeCampaigns}</p>
        </div>

        <div className="card">
          <h3>Total Calls</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#ff9800' }}>{stats.totalCalls}</p>
        </div>

        <div className="card">
          <h3>Completed Calls</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#9c27b0' }}>{stats.completedCalls}</p>
        </div>
      </div>

      <div className="card">
        <h3>Quick Actions</h3>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <a href="/campaigns" className="btn">Manage Campaigns</a>
          <a href="/calls" className="btn">View Calls</a>
          <a href="/analytics" className="btn">View Analytics</a>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
