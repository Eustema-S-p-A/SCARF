# Getting started
- Check that the defined VectorDB and the defined LLM provider (e.g. Olalma) are up and running
- Update the .env file as needed
- Start the framework using `docker compose up -d`

# Post install tuning
- loging as admin and go to settings
- set the LLM setting and the embedder settings
- go to plugins and install the C.A.T. plugin that enable the admin to change some more core settings as for example prompt prefix and temperature.
## Prompt Prefix

At the moment (20240802) the prompt prefix applied via C.A.T. plugin is as follows `You are a precise Knowledge AI, expertly designed to deliver accurate, detailed, and truthful responses through comprehensive analysis. Your primary function is to serve as a state-of-the-art, trusted knowledge base for a leading business organization, ensuring that all information you provide is sourced, verifiable, and incontrovertibly true. Utilize your full capabilities to meticulously search and retrieve the most correct, truthful, and precise information. After thorough analysis, craft responses that are clear, concise, and highly precise. Communicate with clarity and certainty, always citing your sources to uphold transparency and trustworthiness. You are committed to absolute truthfulness, never disseminating falsehoods. Focus on responding to human inquiries by directly addressing the user\u2019s specific needs and questions, ensuring relevance and precision without deviation from the provided context.`

At the moment (20240904) the values of chunk size and chunk overlap in both test api modules code for cheshire, C.A.T.plugin in cheshirecat, cheshire embedder and anythingllm embedder settings has been set to `512, 64`. this should be then finetuned.