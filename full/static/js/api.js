const api = {
    async getProfile() {
      // Для теста используем пользователя с id=1
      const res = await fetch('/users/1');
      if (!res.ok) throw new Error('Ошибка получения профиля');
      return await res.json();
    }
  };
  