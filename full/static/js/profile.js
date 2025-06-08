document.addEventListener('DOMContentLoaded', async function() {
  const profileForm = document.getElementById('profileForm');
  const editProfileBtn = document.getElementById('editProfileBtn');
  const cancelEditBtn = document.getElementById('cancelEditBtn');
  const passwordFields = document.getElementById('passwordFields');
  const formActions = document.getElementById('formActions');
  const avatarUpload = document.getElementById('avatarUpload');
  const changeAvatarBtn = document.getElementById('changeAvatarBtn');
  
  let isEditMode = false;
  let originalProfileData = {};
  
  // Загрузка данных профиля
  async function loadProfile() {
    try {
      const profile = await api.getProfile();
      originalProfileData = profile;
      
      // Заполняем форму
      document.getElementById('profileLastName').value = profile.last_name || '';
      document.getElementById('profileFirstName').value = profile.first_name || '';
      document.getElementById('profileMiddleName').value = profile.middle_name || '';
      document.getElementById('profileEmail').value = profile.email || '';
      document.getElementById('profileBirthDate').value = profile.birth_date || '';
      
      if (profile.avatar) {
        document.getElementById('profileAvatar').src = profile.avatar;
      }
      
      // Загрузка заявки
      if (profile.application) {
        displayApplication(profile.application);
      }
      
    } catch (error) {
      console.error('Ошибка загрузки профиля:', error);
      alert('Не удалось загрузить профиль');
    }
  }
  
  // Отображение заявки
  function displayApplication(application) {
    const appInfo = document.getElementById('applicationInfo');
    appInfo.innerHTML = `
      <div class="application-card">
        <h3 class="application-faculty">${application.faculty_name}</h3>
        <p class="application-status">Статус: <span class="status-${application.status}">${getStatusText(application.status)}</span></p>
        <p class="application-date">Дата подачи: ${new Date(application.created_at).toLocaleDateString()}</p>
        ${application.status === 'pending' ? 
          `<button id="withdrawApplicationBtn" class="btn btn-outline btn-sm">Отозвать заявку</button>` : ''}
      </div>
    `;
  }
  
  function getStatusText(status) {
    const statuses = {
      'pending': 'На рассмотрении',
      'approved': 'Одобрена',
      'rejected': 'Отклонена'
    };
    return statuses[status] || status;
  }
  
  // Переключение режима редактирования
  function toggleEditMode() {
    isEditMode = !isEditMode;
    const inputs = profileForm.querySelectorAll('input[type="text"], input[type="email"], input[type="date"]');
    
    inputs.forEach(input => {
      input.readOnly = !isEditMode;
    });
    
    passwordFields.classList.toggle('hidden', !isEditMode);
    formActions.classList.toggle('hidden', !isEditMode);
    editProfileBtn.classList.toggle('hidden', isEditMode);
    changeAvatarBtn.classList.toggle('hidden', !isEditMode);
  }
  
  // Обработчики событий
  editProfileBtn.addEventListener('click', toggleEditMode);
  cancelEditBtn.addEventListener('click', () => {
    // Восстановление исходных значений
    document.getElementById('profileLastName').value = originalProfileData.last_name;
    document.getElementById('profileFirstName').value = originalProfileData.first_name;
    document.getElementById('profileMiddleName').value = originalProfileData.middle_name;
    document.getElementById('profileEmail').value = originalProfileData.email;
    document.getElementById('profileBirthDate').value = originalProfileData.birth_date;
    
    toggleEditMode();
  });
  
  profileForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
      first_name: document.getElementById('profileFirstName').value,
      last_name: document.getElementById('profileLastName').value,
      middle_name: document.getElementById('profileMiddleName').value,
      birth_date: document.getElementById('profileBirthDate').value,
      email: document.getElementById('profileEmail').value
    };
    
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (newPassword && newPassword !== confirmPassword) {
      alert('Пароли не совпадают');
      return;
    }
    
    if (newPassword) {
      formData.password = newPassword;
    }
    
    try {
      await api.updateProfile(formData);
      await loadProfile();
      toggleEditMode();
      alert('Профиль успешно обновлён');
    } catch (error) {
      console.error('Ошибка обновления профиля:', error);
      alert('Не удалось обновить профиль');
    }
  });
  
  // Загрузка аватарки
  changeAvatarBtn.addEventListener('click', () => avatarUpload.click());
  
  avatarUpload.addEventListener('change', async function() {
    if (!this.files.length) return;
    
    const file = this.files[0];
    const formData = new FormData();
    formData.append('avatar', file);
    
    try {
      const response = await fetch(`${API_BASE_URL}/profile/avatar`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` },
        body: formData
      });
      
      if (!response.ok) throw new Error('Ошибка загрузки аватарки');
      
      const data = await response.json();
      document.getElementById('profileAvatar').src = data.avatar_url;
      alert('Аватар успешно обновлён');
    } catch (error) {
      console.error('Ошибка:', error);
      alert('Не удалось загрузить аватар');
    }
  });
  
  // Инициализация
  await loadProfile();
});