import React, { useState, useEffect} from 'react';
import ZnaniumApi from '../API/API';

async function LectureList() {
	const [lectures, setLectures] = useState()

	useEffect(() => {
		async function getLectures() {
			const response = await ZnaniumApi.getLectures()
			console.log(response.data)
			return response.data
		}
		getLectures().then((lectures) => {
      if (lectures) {
        setLectures(lectures)}
    });
  }, []);

	if (lectures) {
		return (
			<div>
				{lectures.map((lecture, index) => (
					<div key={index} className="lecture">
						<h2>{lecture.lecture_name}</h2>
						<p>{lecture.content}</p>
						<div className="video-links">
							<h3>Video Links:</h3>
							<ul>
								{lecture.video_link.map((link, videoIndex) => (
									<li key={videoIndex}>
										<a href={link} target="_blank" rel="noopener noreferrer">
											{link}
										</a>
									</li>
								))}
							</ul>
						</div>
					</div>
				))}
			</div>
		);
	}
	return <></>
	
};

export default LectureList;
