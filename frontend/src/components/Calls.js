import React, { useState, useEffect } from 'react';
import { callsAPI } from '../services/api';

const Calls = () => {
  const [calls, setCalls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    campaign: '',
    recipient_number: '',
    status: 'pending'
  });

  useEffect(() => {
    fetchCalls();
  }, []);

  const fetchCalls = async () => {
    try {
      const response = await callsAPI.getCalls();
      setCalls(response.data);
    } catch (error) {
      console.error('Error fetching calls:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await callsAPI.createCall(formData);
      setFormData({
        campaign: '',
        recipient_number: '',
        status: 'pending'
      });
      setShowForm(false);
      fetchCalls();
    } catch (error) {
      console.error('Error creating call:', error);
    }
  };

  const handleInitiate = async (id) => {
    try {
      await callsAPI.initiateCall(id);
      fetchCalls();
    } catch (error) {
      console.error('Error initiating call:', error);
    }
  };

  const handleHangup = async (id) => {
    try {
      await callsAPI.hangupCall(id);
      fetchCalls();
    } catch (error) {
      console.error('Error hanging up call:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this call?')) {
      try {
        await callsAPI.deleteCall(id);
        fetchCalls();
      } catch (error) {
        console.error('Error deleting call:', error);
      }
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'completed': return 'status-active';
      case 'failed': return 'status-inactive';
      case 'in_progress': return 'status-pending';
      case 'pending': return 'status-pending';
      default: return '';
    }
  };

  if (loading) {
    return <div className="container">Loading calls...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Calls</h1>
        <button onClick={() => setShowForm(!showForm)} className="btn">
          {showForm ? 'Cancel' : 'Create Call'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3>Create New Call</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Campaign ID:</label>
              <input
                type="number"
                value={formData.campaign}
                onChange={(e) => setFormData({...formData, campaign: e.target.value})}
                placeholder="Enter campaign ID"
                required
              />
            </div>

            <div className="form-group">
              <label>Recipient Number:</label>
              <input
                type="tel"
                value={formData.recipient_number}
                onChange={(e) => setFormData({...formData, recipient_number: e.target.value})}
                required
              />
            </div>

            <button type="submit" className="btn">Create Call</button>
          </form>
        </div>
      )}

      <div className="card">
        <h3>All Calls</h3>
        {calls.length === 0 ? (
          <p>No calls found. Create your first call!</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Campaign</th>
                <th>Recipient</th>
                <th>Status</th>
                <th>Duration</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {calls.map(call => (
                <tr key={call.id}>
                  <td>{call.id}</td>
                  <td>{call.campaign_name || call.campaign}</td>
                  <td>{call.recipient_number}</td>
                  <td className={getStatusClass(call.status)}>
                    {call.status}
                  </td>
                  <td>{call.duration || 'N/A'}</td>
                  <td>{new Date(call.created_at).toLocaleDateString()}</td>
                  <td>
                    {call.status === 'pending' && (
                      <button onClick={() => handleInitiate(call.id)} className="btn">
                        Initiate
                      </button>
                    )}
                    {call.status === 'in_progress' && (
                      <button onClick={() => handleHangup(call.id)} className="btn">
                        Hang Up
                      </button>
                    )}
                    <button onClick={() => handleDelete(call.id)} className="btn btn-danger">
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Calls;
