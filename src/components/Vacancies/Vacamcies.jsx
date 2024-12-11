import React, { useEffect, useState } from 'react';
import './Vacamcies.css';
import ZnaniumApi from '../../API/API';

// Component to display individual vacancy
const Vacancy = ({ vacancy }) => (
  <div className="vacancy">
    <h3>{vacancy.vacancy_name}</h3>
    <p><strong>Description:</strong> {vacancy.description}</p>
    <p><strong>Amount:</strong> {vacancy.amount}</p>
    <p><strong>Company:</strong> {vacancy.company}</p>
    <p><strong>Salary:</strong> {vacancy.salary}</p>
    {/* <p><strong>Contacts:</strong> {vacancy.contacts.join(', ')}</p> */}
  </div>
);


function VacancyList() {
	const [isVis, setIsVis] = useState(false)
	const [vacancies, setVacancies] = useState([''])
	useEffect(() => {
		async function getVacancies() {
			const response = await ZnaniumApi.getVacancies()
			return response.data
		}
		// res = getVacancies()
		getVacancies().then((vacans) => {
			setVacancies(vacans)

		})
	}, [])
	
	function show() {
		setIsVis(isVis === false)
	}

	return (
  <div className="vacancy-list">
		<button onClick={show} >Create New Vacancy</button>
		<CreateVacancyModal isOpen={isVis} onClose={show} ></CreateVacancyModal>
    {vacancies.map((vacancy, index) => (
      <Vacancy key={index} vacancy={vacancy} />
    ))}
  </div>
	)
};


const CreateVacancyModal = ({ isOpen, onClose, onVacancyCreated }) => {
  const [vacancyName, setVacancyName] = useState('');
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState(1);
  const [company, setCompany] = useState('');
  const [salary, setSalary] = useState(0);
  const [contacts, setContacts] = useState(['']);

  const handleAddContact = () => {
    setContacts([...contacts, '']);
  };

  const handleContactChange = (index, value) => {
    const newContacts = [...contacts];
    newContacts[index] = value;
    setContacts(newContacts);
  };

  const handleRemoveContact = (index) => {
    const newContacts = contacts.filter((_, i) => i !== index);
    setContacts(newContacts);
  };

  const handleSubmit = async () => {
    const vacancyData = {
      vacancy_name: vacancyName,
      description,
      amount,
      company,
      salary,
      contacts,
    };

    try {
     await ZnaniumApi.createVacancy(vacancyData)

      onVacancyCreated(vacancyData);
      onClose();
    } catch (error) {
      console.error('Error creating vacancy:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Create Vacancy</h2>
        <div className="modal-content">
          <label>
            Vacancy Name:
            <input
              type="text"
              value={vacancyName}
              onChange={(e) => setVacancyName(e.target.value)}
            />
          </label>
          <label>
            Description:
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </label>
          <label>
            Amount:
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(parseInt(e.target.value))}
            />
          </label>
          <label>
            Company:
            <input
              type="text"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
            />
          </label>
          <label>
            Salary:
            <input
              type="number"
              value={salary}
              onChange={(e) => setSalary(parseInt(e.target.value))}
            />
          </label>
          <label>
            Contacts:
            {contacts.map((contact, index) => (
              <div key={index} className="contact-input">
                <input
                  type="text"
                  value={contact}
                  onChange={(e) => handleContactChange(index, e.target.value)}
                />
                <button type="button" onClick={() => handleRemoveContact(index)}>
                  Remove
                </button>
              </div>
            ))}
            <button type="button" onClick={handleAddContact}>
              Add Contact
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

export { VacancyList, CreateVacancyModal };
