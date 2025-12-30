import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: '', // Your OpenAI API key here
  dangerouslyAllowBrowser: true
});

/**
 * Chỉnh chính tả tiếng Việt bằng GPT-4o-mini
 */
export async function correctVietnameseSpelling(text) {
  if (!text || text.trim().length === 0) {
    return { corrected: text, hasCorrected: false };
  }

  console.log('🟨 ========================================');
  console.log('🟨 [Spellcheck] Input:', text);

  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: `Bạn là trợ lý chỉnh chính tả tiếng Việt chuyên nghiệp. 
Nhiệm vụ: Sửa lỗi chính tả, dấu thanh, dấu câu của văn bản tiếng Việt.
Quy tắc:
- Chỉ sửa lỗi chính tả và dấu thanh, KHÔNG thay đổi ngữ nghĩa
- GIỮ NGUYÊN các từ địa danh, tên riêng của di tích Cần Thơ (như Khám Lớn, Bà Bộ Lão, Chùa Ông, v.v.)
- Trả về ĐÚNG văn bản đã sửa, KHÔNG giải thích, KHÔNG thêm bớt
- Nếu không có lỗi, trả về y nguyên văn bản gốc`
        },
        {
          role: "user",
          content: text
        }
      ],
      temperature: 0.3,
      max_tokens: 200
    });

    const corrected = response.choices[0].message.content.trim();
    const hasCorrected = corrected !== text;

    console.log('🟨 [Spellcheck] Output:', corrected);
    console.log('🟨 [Spellcheck] Changed:', hasCorrected);
    console.log('🟨 ========================================');

    return { corrected, hasCorrected };

  } catch (error) {
    console.error('🟨 [Spellcheck ERROR]:', error);
    console.log('🟨 ========================================');
    return { corrected: text, hasCorrected: false };
  }
}