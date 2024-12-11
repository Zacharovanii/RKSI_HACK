import React, { useState, useEffect} from 'react';
import ZnaniumApi from '../API/API';
import CreateLectureModal from './Modal/Modal';

function LectureList({ roleId }) {
	const [lectures, setLectures] = useState(
		[]
	)
	const [isModalVisible, setIsModalVisible] = useState(false)

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

	const createLecture = () => {
		setIsModalVisible(isModalVisible === false)
	}

	const Menu = () => {
		if (roleId == 4 | roleId == 2) {
			return (
				<>
					<button onClick={createLecture} >Add lecture</button>
					<CreateLectureModal isOpen={isModalVisible} onClose={createLecture} ></CreateLectureModal>
				</>
			)
		}
		return <></>
	}

	if (lectures) {
		return (
			<div>
				<Menu/>
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
