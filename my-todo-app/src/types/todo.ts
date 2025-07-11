export interface Todo {
  id: string;
  task: string;
  status: 'pending' | 'completed';
  category?: string;
  due_date?: string;    // or Date, depending on your parsing
  tags?: string[];
  user_id: number;
}