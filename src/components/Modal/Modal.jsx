import React, { useState } from 'react';
import ZnaniumApi from '../../API/API';
import './Modal.css';

const CreateLectureModal = ({ isOpen, onClose
}) => {
  const [lectureName, setLectureName] = useState('');
  const [content, setContent] = useState('');
  const [videoLinks, setVideoLinks] = useState(['']);

  const handleAddVideoLink = () => {
    setVideoLinks([...videoLinks, '']);
  };

  const handleVideoLinkChange = (index, value) => {
    const newVideoLinks = [...videoLinks];
    newVideoLinks[index] = value;
    setVideoLinks(newVideoLinks);
  };

  const handleRemoveVideoLink = (index) => {
    const newVideoLinks = videoLinks.filter((_, i) => i !== index);
    setVideoLinks(newVideoLinks);
  };

  const handleSubmit = async () => {
    const lectureData = {
      lecture_name: lectureName,
      content,
      video_links: videoLinks,
    };

    try {
      const response = await ZnaniumApi.createLecture(lectureData)
    } catch (error) {
      console.error('Error creating lecture:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Create Lecture</h2>
        <div className="modal-content">
          <label>
            Lecture Name:
            <input
              type="text"
              value={lectureName}
              onChange={(e) => setLectureName(e.target.value)}
            />
          </label>
          <label>
            Content:
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
          </label>
          <label>
            Video Links:
            {videoLinks.map((link, index) => (
              <div key={index} className="video-link-input">
                <input
                  type="url"
                  value={link}
                  onChange={(e) => handleVideoLinkChange(index, e.target.value)}
                  placeholder="https://example.com"
                />
                <button type="button" onClick={() => handleRemoveVideoLink(index)}>
                  Remove
                </button>
              </div>
            ))}
            <button type="button" onClick={handleAddVideoLink}>
              Add Video Link
            </button>
          </label>
        </div>
        <div className="modal-actions">
          <button type="button" onClick={handleSubmit}>
            Submit
          </button>
          <button type="button" onClick={onClose}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateLectureModal;
