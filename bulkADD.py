import sqlite3

def connect_to_db():
    """Connect to SQLite database and return connection and cursor."""
    conn = sqlite3.connect("posts.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post TEXT NOT NULL,
            category TEXT,
            response TEXT,
            harmful_content BOOLEAN DEFAULT NULL
        )
    """)
    conn.commit()
    return conn, cursor


def add_posts_to_db(posts):
    """Add multiple posts to the database with NULL category."""
    conn, cursor = connect_to_db()  # Establish connection using imported function
    try:
        # Prepare data for batch insertion, extracting only the post text
        posts_data = [(post["post"], None, None) for post in posts]
        
        # Insert multiple posts at once
        cursor.executemany("INSERT INTO posts (post, category, response) VALUES (?, ?, ?)", posts_data)
        conn.commit()  # Save changes to the database
        print(f"{len(posts)} posts added.")
    except sqlite3.Error as e:
        print(f"Error adding posts to database: {e}")
    finally:
        conn.close()  # Ensure the connection is closed

def main():
    """Function to handle batch insertion of posts."""

    posts = [
        {"post": "اليوم كنت أتابع الوضع السياسي في المنطقة، والتحديات الكبيرة اللي بنواجهها في تحسين الوضع الاقتصادي.", "category": None},
        {"post": "في الآونة الأخيرة، حصلت تغييرات كبيرة في القوانين المتعلقة بحرية التعبير في بعض الدول.", "category": None},
        {"post": "الوضع السياسي في بلدي حاليًا يحتاج إلى إصلاحات جذرية لتحسين جودة الحياة للمواطنين.", "category": None},
        {"post": "لاحظت أن الحوار السياسي في الفترة الأخيرة أصبح أكثر جدية، وأتمنى أن يستمر هذا التوجه.", "category": None},
        {"post": "التحديات السياسية في الشرق الأوسط تتطلب تعاون أكبر بين الدول لتحقيق الاستقرار.", "category": None},
        {"post": "اليوم كنت أقرأ عن تأثير السياسة الاقتصادية على الطبقات الاجتماعية المختلفة، والفجوة بينهم بتكبر.", "category": None},
        {"post": "أعتقد أنه من الضروري زيادة الوعي بالحقوق السياسية في المجتمعات المختلفة.", "category": None},
        {"post": "الانتخابات القادمة في بلدي قد تكون حاسمة في تحديد شكل الحكومة المستقبلية.", "category": None},
        {"post": "الأزمات السياسية في الدول النامية تستدعي تدخلات دولية لتحسين الوضع الأمني والاقتصادي.", "category": None},
        {"post": "بعض الدول تتجه لتطبيق قوانين أكثر صرامة للحد من الفساد السياسي، وهو أمر إيجابي للغاية.", "category": None},
        {"post": "الحوار السياسي بين الأحزاب المختلفة في بلدي أصبح أكثر تعقيدًا بسبب التحديات الحالية.", "category": None},
        {"post": "في المستقبل القريب، أعتقد أنه سيكون هناك تغييرات كبيرة في سياسات الهجرة في أوروبا.", "category": None},
        {"post": "حلمت بتغييرات إيجابية في السياسات الاجتماعية التي تحسن حياة الناس وتحقق العدالة الاجتماعية.", "category": None},
        {"post": "أصبح من المهم جدًا أن تكون هناك سياسات شاملة تعزز التعاون بين الحكومة والشعب لتحقيق التنمية المستدامة.", "category": None},
        {"post": "التدخلات العسكرية في بعض المناطق أصبحت قضية شائكة، وهناك نقاشات حادة حول فعاليتها.", "category": None},
        {"post": "اتفق الجميع على ضرورة تقوية العلاقات الدبلوماسية بين الدول العربية لتحسين الوضع الإقليمي.", "category": None},
        {"post": "مؤتمر الأمم المتحدة الأخير ركز على الأزمات الإنسانية في بعض المناطق، وكان له تأثير كبير على السياسيين.", "category": None},
        {"post": "التعديلات الدستورية في بعض البلدان تحتاج إلى مزيد من النقاشات لتأمين الحقوق الأساسية للمواطنين.", "category": None},
        {"post": "هناك ضرورة كبيرة لتحسين الشفافية في الانتخابات لضمان نزاهتها وتحقيق العدالة.", "category": None},
        {"post": "الاقتصاد والسياسة مرتبطين بشكل وثيق، ولا بد من حل الأزمات السياسية لتخفيف التحديات الاقتصادية.", "category": None}
    ]


    
    # Add all posts in the list to the database
    add_posts_to_db(posts)

if __name__ == "__main__":
    main()
