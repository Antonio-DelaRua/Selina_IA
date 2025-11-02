"""
Interfaz de calendario para gestión de tareas
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import calendar as cal
import datetime
from core.database import Task, SessionLocal
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT

class CalendarWindow:
    def __init__(self, parent):
        self.parent = parent
        self.current_date = datetime.date.today()
        self.selected_date = self.current_date

        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title("📅 Calendario de Tareas - NoBt")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.configure(bg='white')

        # Configurar grid
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Header con navegación
        self.create_header()

        # Área principal dividida
        main_frame = tk.Frame(self.window, bg='white')
        main_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_rowconfigure(0, weight=1)

        # Calendario mensual
        self.create_calendar_view(main_frame)

        # Panel lateral de tareas
        self.create_tasks_panel(main_frame)

        # Cargar datos iniciales
        self.refresh_calendar()
        self.load_tasks_for_date(self.selected_date)

        # Auto-refresh cada 30 segundos
        self.schedule_auto_refresh()

    def create_header(self):
        """Crear header con navegación de meses"""
        header = tk.Frame(self.window, bg='#f0f0f0', height=60)
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)

        # Botón mes anterior
        prev_btn = tk.Button(header, text="◀", font=("Arial", 16, "bold"),
                           command=self.previous_month, bg='#f0f0f0', relief='flat')
        prev_btn.pack(side='left', padx=20)

        # Título del mes/año
        self.month_year_label = tk.Label(header, text="", font=("Arial", 18, "bold"),
                                       bg='#f0f0f0', fg='#333')
        self.month_year_label.pack(side='left', expand=True)

        # Botón mes siguiente
        next_btn = tk.Button(header, text="▶", font=("Arial", 16, "bold"),
                           command=self.next_month, bg='#f0f0f0', relief='flat')
        next_btn.pack(side='right', padx=20)

        # Botón Hoy
        today_btn = tk.Button(header, text="📅 Hoy", command=self.go_to_today,
                            bg='#007acc', fg='white', font=("Arial", 10))
        today_btn.pack(side='right', padx=10)

    def create_calendar_view(self, parent):
        """Crear vista del calendario mensual"""
        calendar_frame = tk.Frame(parent, bg='white')
        calendar_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 20))

        # Días de la semana
        days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        for i, day in enumerate(days):
            tk.Label(calendar_frame, text=day, font=("Arial", 12, "bold"),
                    bg='white', fg='#666').grid(row=0, column=i, padx=5, pady=5)

        # Grid de días (6 filas x 7 columnas máximo)
        self.day_buttons = []
        for row in range(6):
            for col in range(7):
                btn = tk.Button(calendar_frame, text="", width=4, height=2,
                              font=("Arial", 11), relief='flat', bg='white',
                              command=lambda r=row, c=col: self.day_clicked(r, c))
                btn.grid(row=row+1, column=col, padx=2, pady=2, sticky='nsew')
                self.day_buttons.append(btn)

    def create_tasks_panel(self, parent):
        """Crear panel lateral de tareas"""
        tasks_frame = tk.Frame(parent, bg='#f8f9fa', width=300)
        tasks_frame.grid(row=0, column=1, sticky='ns', padx=(20, 0))
        tasks_frame.grid_propagate(False)

        # Título
        title_label = tk.Label(tasks_frame, text="📋 Tareas del Día",
                             font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#333')
        title_label.pack(pady=10)

        # Fecha seleccionada
        self.selected_date_label = tk.Label(tasks_frame, text="",
                                          font=("Arial", 12), bg='#f8f9fa', fg='#666')
        self.selected_date_label.pack(pady=(0, 10))

        # Lista de tareas
        list_frame = tk.Frame(tasks_frame, bg='#f8f9fa')
        list_frame.pack(fill='both', expand=True, padx=10)

        # Scrollbar para tareas
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        self.tasks_canvas = tk.Canvas(list_frame, bg='#f8f9fa', yscrollcommand=scrollbar.set)
        self.tasks_canvas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tasks_canvas.yview)

        self.tasks_frame = tk.Frame(self.tasks_canvas, bg='#f8f9fa')
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor='nw')

        # Botones de acción
        buttons_frame = tk.Frame(tasks_frame, bg='#f8f9fa')
        buttons_frame.pack(fill='x', pady=10)

        add_btn = tk.Button(buttons_frame, text="➕ Agregar Tarea",
                          command=self.add_task, bg='#28a745', fg='white',
                          font=("Arial", 10))
        add_btn.pack(fill='x', pady=2)

        refresh_btn = tk.Button(buttons_frame, text="🔄 Actualizar",
                              command=lambda: self.load_tasks_for_date(self.selected_date),
                              bg='#6c757d', fg='white', font=("Arial", 10))
        refresh_btn.pack(fill='x', pady=2)

    def refresh_calendar(self):
        """Actualizar la vista del calendario"""
        # Actualizar título
        month_name = cal.month_name[self.current_date.month]
        self.month_year_label.config(text=f"{month_name} {self.current_date.year}")

        # Obtener calendario del mes
        cal_obj = cal.monthcalendar(self.current_date.year, self.current_date.month)

        # Limpiar botones anteriores
        for btn in self.day_buttons:
            btn.config(text="", bg='white', fg='black', state='normal')

        # Llenar con días del mes
        day_num = 0
        for week in range(6):
            for day in range(7):
                if day_num < len(cal_obj[week]) and cal_obj[week][day] != 0:
                    day_value = cal_obj[week][day]
                    btn = self.day_buttons[week * 7 + day]
                    btn.config(text=str(day_value))

                    # Resaltar día actual
                    current_day = datetime.date.today()
                    if (self.current_date.year == current_day.year and
                        self.current_date.month == current_day.month and
                        day_value == current_day.day):
                        btn.config(bg='#e3f2fd', fg='#1976d2')

                    # Resaltar día seleccionado
                    if (self.current_date.year == self.selected_date.year and
                        self.current_date.month == self.selected_date.month and
                        day_value == self.selected_date.day):
                        btn.config(bg='#fff3e0', fg='#f57c00')

                    # Marcar días con tareas
                    task_date = datetime.date(self.current_date.year, self.current_date.month, day_value)
                    if self.has_tasks(task_date):
                        btn.config(bg='#c8e6c9', fg='#2e7d32')

    def has_tasks(self, date):
        """Verificar si una fecha tiene tareas"""
        tasks = Task.get_tasks_for_date(date)
        return len(tasks) > 0

    def day_clicked(self, row, col):
        """Manejar clic en un día del calendario"""
        cal_obj = cal.monthcalendar(self.current_date.year, self.current_date.month)
        if row < len(cal_obj) and col < len(cal_obj[row]):
            day = cal_obj[row][col]
            if day != 0:
                self.selected_date = datetime.date(self.current_date.year, self.current_date.month, day)
                self.refresh_calendar()
                self.load_tasks_for_date(self.selected_date)

    def load_tasks_for_date(self, date):
        """Cargar tareas para una fecha específica"""
        # Actualizar etiqueta de fecha
        date_str = date.strftime("%d/%m/%Y")
        weekday = cal.day_name[date.weekday()]
        self.selected_date_label.config(text=f"{weekday} {date_str}")

        # Limpiar tareas anteriores
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        # Obtener tareas
        tasks = Task.get_tasks_for_date(date)

        if not tasks:
            no_tasks_label = tk.Label(self.tasks_frame,
                                    text="📝 No hay tareas para este día",
                                    font=("Arial", 11), bg='#f8f9fa', fg='#666')
            no_tasks_label.pack(pady=20)
            return

        # Mostrar tareas
        for task in tasks:
            self.create_task_widget(task)

        # Actualizar scroll region
        self.tasks_frame.update_idletasks()
        self.tasks_canvas.config(scrollregion=self.tasks_canvas.bbox("all"))

    def create_task_widget(self, task):
        """Crear widget para una tarea"""
        # Frame contenedor
        task_frame = tk.Frame(self.tasks_frame, bg='white', relief='solid', bd=1)
        task_frame.pack(fill='x', pady=2, padx=5)

        # Checkbox para completar
        var = tk.BooleanVar(value=bool(task.completed))
        checkbox = tk.Checkbutton(task_frame, variable=var,
                                command=lambda: self.toggle_task(task, var))
        checkbox.pack(side='left', padx=5)

        # Contenido de la tarea
        content_frame = tk.Frame(task_frame, bg='white')
        content_frame.pack(side='left', fill='x', expand=True, padx=5)

        # Título
        title_label = tk.Label(content_frame, text=task.title,
                             font=("Arial", 11, "bold"), bg='white',
                             fg='#333', anchor='w')
        title_label.pack(fill='x')

        # Descripción (si existe)
        if task.description:
            desc_label = tk.Label(content_frame, text=task.description[:50] + "..." if len(task.description) > 50 else task.description,
                                font=("Arial", 9), bg='white', fg='#666', anchor='w')
            desc_label.pack(fill='x')

        # Hora y prioridad
        info_frame = tk.Frame(content_frame, bg='white')
        info_frame.pack(fill='x')

        time_text = f"🕐 {task.time}" if task.time else ""
        priority_colors = {'high': '#dc3545', 'medium': '#ffc107', 'low': '#28a745'}
        priority_text = f"⚡ {task.priority.capitalize()}"

        if time_text or priority_text:
            info_label = tk.Label(info_frame, text=f"{time_text} {priority_text}",
                                font=("Arial", 8), bg='white',
                                fg=priority_colors.get(task.priority, '#666'))
            info_label.pack(side='left')

        # Botón eliminar
        delete_btn = tk.Button(task_frame, text="🗑️",
                             command=lambda: self.delete_task(task),
                             bg='white', relief='flat', font=("Arial", 10))
        delete_btn.pack(side='right', padx=5)

        # Tachar si completada
        if task.completed:
            title_label.config(fg='#999')
            if task.description:
                desc_label.config(fg='#ccc')

    def toggle_task(self, task, var):
        """Alternar estado de completado de tarea"""
        session = SessionLocal()
        try:
            db_task = session.query(Task).filter(Task.id == task.id).first()
            if db_task:
                db_task.completed = 1 if var.get() else 0
                session.commit()
                self.load_tasks_for_date(self.selected_date)  # Recargar
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tarea: {e}")
        finally:
            session.close()

    def delete_task(self, task):
        """Eliminar una tarea"""
        if messagebox.askyesno("Confirmar", f"¿Eliminar la tarea '{task.title}'?"):
            session = SessionLocal()
            try:
                db_task = session.query(Task).filter(Task.id == task.id).first()
                if db_task:
                    session.delete(db_task)
                    session.commit()
                    self.load_tasks_for_date(self.selected_date)  # Recargar
                    self.refresh_calendar()  # Actualizar indicadores
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la tarea: {e}")
            finally:
                session.close()

    def add_task(self):
        """Agregar nueva tarea"""
        # Diálogo para nueva tarea
        title = simpledialog.askstring("Nueva Tarea", "Título de la tarea:")
        if not title:
            return

        description = simpledialog.askstring("Nueva Tarea", "Descripción (opcional):")
        time_str = simpledialog.askstring("Nueva Tarea", "Hora (HH:MM, opcional):")

        # Crear tarea
        session = SessionLocal()
        try:
            new_task = Task(
                title=title,
                description=description or "",
                date=datetime.datetime.combine(self.selected_date, datetime.time.min),
                time=time_str if time_str else None,
                priority='medium',
                completed=0,
                category='personal'
            )
            session.add(new_task)
            session.commit()

            self.load_tasks_for_date(self.selected_date)  # Recargar
            self.refresh_calendar()  # Actualizar indicadores

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la tarea: {e}")
        finally:
            session.close()

    def previous_month(self):
        """Ir al mes anterior"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.refresh_calendar()

    def next_month(self):
        """Ir al mes siguiente"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.refresh_calendar()

    def go_to_today(self):
        """Ir al mes actual"""
        self.current_date = datetime.date.today()
        self.selected_date = self.current_date
        self.refresh_calendar()
        self.load_tasks_for_date(self.selected_date)

    def schedule_auto_refresh(self):
        """Programar actualización automática cada 30 segundos"""
        try:
            if self.window.winfo_exists():
                self.refresh_calendar()
                self.load_tasks_for_date(self.selected_date)
                # Programar siguiente actualización
                self.window.after(30000, self.schedule_auto_refresh)  # 30 segundos
        except Exception as e:
            # Si hay error, intentar de nuevo en 30 segundos
            try:
                if self.window.winfo_exists():
                    self.window.after(30000, self.schedule_auto_refresh)
            except:
                pass  # Ventana cerrada, no hacer nada